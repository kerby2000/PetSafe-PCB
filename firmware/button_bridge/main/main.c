#include <inttypes.h>
#include <stdio.h>
#include <string.h>
#include "bridge_policy.h"
#include "button_output.h"
#include "esp_event.h"
#include "esp_http_server.h"
#include "esp_log.h"
#include "esp_netif.h"
#include "esp_random.h"
#include "esp_timer.h"
#include "esp_wifi.h"
#include "nvs_flash.h"

#if __has_include("credentials.local.h")
#include "credentials.local.h"
#else
#define BRIDGE_WIFI_SSID ""
#define BRIDGE_WIFI_PASSWORD ""
#define BRIDGE_API_TOKEN ""
#endif

static const char *TAG = "button_bridge";
static bridge_policy_t policy;
static esp_timer_handle_t reconnect_timer;
static uint32_t reconnect_delay_s = 1;

extern const char index_start[] asm("_binary_index_html_start");
extern const char index_end[] asm("_binary_index_html_end");
extern const char script_start[] asm("_binary_app_js_start");
extern const char script_end[] asm("_binary_app_js_end");

static uint64_t now_ms(void) { return (uint64_t)esp_timer_get_time() / 1000; }

static void response_headers(httpd_req_t *req)
{
    httpd_resp_set_hdr(req, "Cache-Control", "no-store");
    httpd_resp_set_hdr(req, "X-Content-Type-Options", "nosniff");
    httpd_resp_set_hdr(req, "Referrer-Policy", "no-referrer");
    httpd_resp_set_hdr(req, "Content-Security-Policy",
        "default-src 'none'; script-src 'self'; style-src 'unsafe-inline'; "
        "connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'");
}

static esp_err_t json_reply(httpd_req_t *req, const char *status, const char *json)
{
    response_headers(req);
    httpd_resp_set_status(req, status);
    httpd_resp_set_type(req, "application/json");
    return httpd_resp_send(req, json, HTTPD_RESP_USE_STRLEN);
}

static bool authorized(httpd_req_t *req)
{
    char header[136];
    if (httpd_req_get_hdr_value_str(req, "Authorization", header, sizeof(header)) == ESP_OK &&
        bridge_authorized(header, BRIDGE_API_TOKEN)) return true;
    httpd_resp_set_hdr(req, "WWW-Authenticate", "Bearer");
    json_reply(req, "401 Unauthorized", "{\"error\":\"unauthorized\"}");
    return false;
}

static esp_err_t page_handler(httpd_req_t *req)
{
    response_headers(req);
    httpd_resp_set_type(req, "text/html; charset=utf-8");
    return httpd_resp_send(req, index_start, index_end - index_start - 1);
}

static esp_err_t script_handler(httpd_req_t *req)
{
    response_headers(req);
    httpd_resp_set_type(req, "text/javascript; charset=utf-8");
    return httpd_resp_send(req, script_start, script_end - script_start - 1);
}

static esp_err_t status_handler(httpd_req_t *req)
{
    if (!authorized(req)) return ESP_OK;
    uint64_t now = now_ms();
    uint64_t wait = policy.available_at_ms > now ? policy.available_at_ms - now : 0;
    char json[512];
    snprintf(json, sizeof(json),
        "{\"firmware\":\"0.1.0\",\"boot_id\":\"%s\",\"uptime_ms\":%" PRIu64
        ",\"next_sequence\":%" PRIu64 ",\"last_sequence\":%" PRIu32
        ",\"command_deadline_ms\":%" PRIu64 ",\"pulse_ms\":%u,"
        "\"cooldown_remaining_ms\":%" PRIu64 ",\"button_active\":%s,"
        "\"door_state\":\"unknown\",\"power_mode\":\"always_on\"}",
        policy.boot_id, now, (uint64_t)policy.last_sequence + 1, policy.last_sequence,
        now + 5000, BRIDGE_PULSE_MS, wait, button_output_active() ? "true" : "false");
    return json_reply(req, "200 OK", json);
}

static bool uint_header(httpd_req_t *req, const char *name, uint64_t limit, uint64_t *value)
{
    char text[24];
    return httpd_req_get_hdr_value_str(req, name, text, sizeof(text)) == ESP_OK &&
           bridge_parse_uint(text, limit, value);
}

static esp_err_t press_handler(httpd_req_t *req)
{
    if (!authorized(req)) return ESP_OK;
    char boot[BRIDGE_BOOT_ID_LEN + 1];
    uint64_t sequence, deadline;
    /* No request body: the three command headers form a bounded, replay-resistant request. */
    if (req->content_len != 0 ||
        httpd_req_get_hdr_value_len(req, "Transfer-Encoding") != 0 ||
        httpd_req_get_hdr_value_str(req, "X-Bridge-Boot", boot, sizeof(boot)) != ESP_OK ||
        strlen(boot) != BRIDGE_BOOT_ID_LEN ||
        !uint_header(req, "X-Bridge-Sequence", UINT32_MAX, &sequence) ||
        !uint_header(req, "X-Bridge-Deadline", UINT64_MAX, &deadline)) {
        httpd_resp_set_hdr(req, "Connection", "close");
        json_reply(req, "400 Bad Request", "{\"error\":\"invalid_command_headers_or_body\"}");
        return ESP_FAIL;
    }
    uint64_t now = now_ms();
    bridge_decision_t decision = bridge_policy_check(&policy, boot, sequence, deadline, now);
    if (decision == BRIDGE_DUPLICATE)
        return json_reply(req, "200 OK", "{\"result\":\"duplicate_no_new_press\"}");
    if (decision == BRIDGE_COOLDOWN) {
        httpd_resp_set_hdr(req, "Retry-After", "5");
        return json_reply(req, "429 Too Many Requests", "{\"error\":\"cooldown_no_press\"}");
    }
    if (decision != BRIDGE_ACCEPT) {
        const char *error = decision == BRIDGE_WRONG_BOOT ? "{\"error\":\"boot_changed_no_press\"}" :
            decision == BRIDGE_EXPIRED ? "{\"error\":\"expired_command_no_press\"}" :
            "{\"error\":\"sequence_conflict_no_press\"}";
        return json_reply(req, "409 Conflict", error);
    }
    if (button_output_press() != ESP_OK)
        return json_reply(req, "503 Service Unavailable", "{\"error\":\"pulse_not_started\"}");
    bridge_policy_commit(&policy, sequence, now);
    ESP_LOGI(TAG, "Button pulse accepted, sequence=%" PRIu32, (uint32_t)sequence);
    return json_reply(req, "202 Accepted", "{\"result\":\"pulse_started\",\"pulse_ms\":200,\"door_state\":\"unknown\"}");
}

static void server_start(void)
{
    httpd_config_t config = HTTPD_DEFAULT_CONFIG();
    config.stack_size = 6144;
    config.recv_wait_timeout = 3;
    config.send_wait_timeout = 3;
    config.lru_purge_enable = true;
    httpd_handle_t server;
    ESP_ERROR_CHECK(httpd_start(&server, &config));
    const httpd_uri_t routes[] = {
        {.uri = "/", .method = HTTP_GET, .handler = page_handler},
        {.uri = "/app.js", .method = HTTP_GET, .handler = script_handler},
        {.uri = "/api/status", .method = HTTP_GET, .handler = status_handler},
        {.uri = "/api/press", .method = HTTP_POST, .handler = press_handler},
    };
    for (size_t i = 0; i < sizeof(routes) / sizeof(routes[0]); ++i)
        ESP_ERROR_CHECK(httpd_register_uri_handler(server, &routes[i]));
}

static void reconnect(void *arg)
{
    (void)arg;
    esp_err_t result = esp_wifi_connect();
    if (result != ESP_OK && result != ESP_ERR_WIFI_CONN)
        ESP_LOGW(TAG, "Wi-Fi retry: %s", esp_err_to_name(result));
}

static void wifi_event(void *arg, esp_event_base_t base, int32_t id, void *data)
{
    (void)arg;
    if (base == WIFI_EVENT && id == WIFI_EVENT_STA_START) {
        ESP_ERROR_CHECK(esp_wifi_connect());
    } else if (base == WIFI_EVENT && id == WIFI_EVENT_STA_DISCONNECTED) {
        /* Reconnection never creates or replays a button command. */
        esp_timer_stop(reconnect_timer);
        ESP_ERROR_CHECK(esp_timer_start_once(reconnect_timer, reconnect_delay_s * 1000000ULL));
        if (reconnect_delay_s < 30) {
            reconnect_delay_s *= 2;
            if (reconnect_delay_s > 30) reconnect_delay_s = 30;
        }
        ESP_LOGW(TAG, "Wi-Fi disconnected; button commands are not queued");
    } else if (base == IP_EVENT && id == IP_EVENT_STA_GOT_IP) {
        esp_timer_stop(reconnect_timer);
        reconnect_delay_s = 1;
        ip_event_got_ip_t *event = data;
        ESP_LOGI(TAG, "Open http://" IPSTR "/ (token required)", IP2STR(&event->ip_info.ip));
    }
}

void app_main(void)
{
    /* Before NVS, networking, credentials or logs: release the physical button. */
    button_output_init();
    size_t ssid_len = strlen(BRIDGE_WIFI_SSID);
    size_t password_len = strlen(BRIDGE_WIFI_PASSWORD);
    size_t token_len = strlen(BRIDGE_API_TOKEN);
    if (ssid_len == 0 || ssid_len > 32 || password_len < 8 || password_len > 63 ||
        token_len < 32 || token_len > 128) {
        ESP_LOGE(TAG, "Not configured. Run configure.py and rebuild. GPIO3 remains LOW; Wi-Fi is off.");
        return;
    }
    ESP_ERROR_CHECK(nvs_flash_init());
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    esp_netif_t *sta = esp_netif_create_default_wifi_sta();
    ESP_ERROR_CHECK(esp_netif_set_hostname(sta, "petsafe-bridge"));
    wifi_init_config_t init = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&init));
    /* esp_fill_random uses RF entropy once Wi-Fi is started. */
    ESP_ERROR_CHECK(esp_wifi_set_storage(WIFI_STORAGE_RAM));
    wifi_config_t wifi = {0};
    memcpy(wifi.sta.ssid, BRIDGE_WIFI_SSID, ssid_len);
    memcpy(wifi.sta.password, BRIDGE_WIFI_PASSWORD, password_len);
    wifi.sta.threshold.authmode = WIFI_AUTH_WPA2_PSK;
    wifi.sta.sae_pwe_h2e = WPA3_SAE_PWE_BOTH;
    const esp_timer_create_args_t retry = {.callback = reconnect, .name = "wifi_reconnect"};
    ESP_ERROR_CHECK(esp_timer_create(&retry, &reconnect_timer));
    ESP_ERROR_CHECK(esp_event_handler_register(WIFI_EVENT, ESP_EVENT_ANY_ID, wifi_event, NULL));
    ESP_ERROR_CHECK(esp_event_handler_register(IP_EVENT, IP_EVENT_STA_GOT_IP, wifi_event, NULL));
    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_STA, &wifi));
    ESP_ERROR_CHECK(esp_wifi_start());
    ESP_ERROR_CHECK(esp_wifi_set_ps(WIFI_PS_MIN_MODEM));
    uint8_t random[16];
    char boot_id[BRIDGE_BOOT_ID_LEN + 1];
    esp_fill_random(random, sizeof(random));
    for (unsigned i = 0; i < sizeof(random); ++i) snprintf(boot_id + 2 * i, 3, "%02x", random[i]);
    bridge_policy_init(&policy, boot_id);
    server_start();
    ESP_LOGI(TAG, "Ready: GPIO3, 200 ms press, 5 s cooldown; no PIR or timer power switching");
}
