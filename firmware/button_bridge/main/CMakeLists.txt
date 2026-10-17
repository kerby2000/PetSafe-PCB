idf_component_register(SRCS "main.c" "bridge_policy.c" "button_output.c"
    INCLUDE_DIRS "."
    PRIV_REQUIRES esp_driver_gpio esp_driver_gptimer esp_http_server esp_wifi
                  esp_netif esp_event esp_timer esp_system nvs_flash esp_hw_support
    EMBED_TXTFILES "web/index.html" "web/app.js")
# Rebuild when configure.py creates the previously absent local header as well as
# when existing credentials change. No secrets are passed as compiler flags.
file(GLOB local_credentials CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/credentials.local.h")
if(local_credentials)
    target_compile_definitions(${COMPONENT_LIB} PRIVATE BRIDGE_HAS_LOCAL_CREDENTIALS=1)
endif()
