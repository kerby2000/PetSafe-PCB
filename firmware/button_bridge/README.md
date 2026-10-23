# PetSafe ESP32-C6 button firmware

Version **0.1.0** implements the owner's perfboard circuit: **GPIO3 → 4.7 kΩ → 2N3904 base**, 100 kΩ base-to-emitter, collector to H_BUTTON/S1.2, emitter to shared GND/S1.1. The physical button remains available. [Wiring and power qualifications](../../docs/BUTTON_BRIDGE.md).

The owner selected **a local web page plus HTTP API**, with Wi-Fi continuously available. TPL5111, PIR wake, deep sleep, converter enable control, camera analysis and absolute OPEN/CLOSE commands are **not implemented**. The firmware cannot determine the latch position or detect a manual button press. A power cycle does not restore a guessed door state.

## Behavior

- GPIO3 is set LOW before enabling its output driver, before networking or configuration checks. No press on startup, page load, Wi-Fi reconnect or reset recovery.
- An authenticated, explicit command produces one **200 ms HIGH pulse**. The owner reports that commands from this firmware produce the expected motor/button behavior; pulse width has not been independently measured and is not a manufacturer timing specification.
- The timer starts before the HIGH write. A short critical section serializes timer start and assertion with the release ISR, so a release cannot be followed by a late HIGH. A failed start never asserts GPIO3. The GPTimer release callback, GPIO operation and timer controls are placed in IRAM. This is not an external hardware interlock against every CPU failure.
- Five-second cooldown, no overlapping presses and no command queue. Rejected commands do not execute later.
- Each command carries the current random boot identifier, the next sequence number, and a deadline based on the ESP's uptime. A valid attempt consumes its sequence **before any output operation**, even if arming, assertion or release fails. Retrying that sequence does not pulse again; older sequences and commands from previous boots are rejected. Missing/invalid/expired commands never actuate.
- Driver failures latch `output_fault` and inhibit further output attempts until restart. A failed HIGH write is reported as an uncertain outcome, since the pin may have changed before the error. A failed LOW write is not reported as released. Inspect the board before restarting; no automatic reset or retry clears the fault.
- Wi-Fi reconnects with 1–30 second backoff. Modem power saving is enabled, but **the ESP remains powered**. No external converter is switched by the firmware. The owner now prefers wired USB power; battery life is unmeasured.
- No credentials: GPIO3 stays LOW and Wi-Fi stays off. No open setup hotspot or default access token.

## Build and configure

Tested toolchain: **ESP-IDF v6.0.2**, target **esp32c6**. No Arduino or third-party firmware libraries are required. Defaults use DIO, 40 MHz flash, **4 MB flash** and native USB Serial/JTAG console. COM3 identified the owned board as ESP32-C6FH4 rev0.1 with 4 MB flash on 2026-10-18; this was checked using esptool, independently of the imported footprint.

Install **ESP-IDF v6.0.2** using Espressif's [Windows setup instructions](https://docs.espressif.com/projects/esp-idf/en/v6.0.2/esp32c6/get-started/windows-setup.html), and open its configured ESP-IDF PowerShell. From your repository root:

```powershell
Set-Location firmware/button_bridge
python configure.py
idf.py build
```

`configure.py` prompts for your 2.4 GHz WPA2/WPA3-personal SSID and password, generates a random access token, and writes `credentials.local.json` plus `main/credentials.local.h`. Both are ignored by Git. It does not print the password or token. Open the JSON locally to copy the token into the web page. To change credentials, edit that local JSON, rerun `configure.py`, and rebuild. The binary contains these credentials: do not publish your configured binary or build directory.

Building without that local header produces an unconfigured image with its output released and networking disabled. A build verifies compilation, not electrical behavior on the owned board.

## Flash or update a prototype

First flash the **ESP board by itself**, with its external converter supply disconnected. Use the actual serial port in place of `COMx`:

```powershell
idf.py -p COMx flash monitor
```

If automatic bootloader entry fails, hold BOOT while connecting USB or resetting, then release BOOT and retry. The native USB serial port can change during reset. Exit the monitor with Ctrl+]. There is no OTA updater in this version.

The console prints `Open http://<assigned-IP>/`. Open that address, enter the access token, and select **Connect**. Connecting only reads status. Consider a router DHCP reservation for the camera controller. `petsafe-bridge` is the DHCP hostname; this firmware does not advertise mDNS, so `.local` resolution is not promised.

The current preference is wired USB power; see [power arrangements and remaining qualifications](../../docs/BUTTON_BRIDGE.md#current-wired-power-direction). For any later battery operation, disconnect USB and use a qualified regulated supply. The earlier LM2596 battery-converter proposal is not the installed supply route. The owner now confirms USB-C into the ESP, its 5V pad to PetSafe battery-positive, all cells removed and converter output disconnected. Any future converter/direct-3V3 arrangement still needs separate input/backfeed qualification. Do not power the ESP load from the PIR rail or factory 4.5 V rail.

## Commissioning

The sequence below remains a reference for future assemblies and failure/restart checks. Completed first-flash and owner functional tests are recorded below; no repeat reconstruction measurements are requested:

1. With the collector disconnected from H_BUTTON, check that GPIO3/base remain released through startup, reset and Wi-Fi loss. A configured board should only pulse after an explicit command.
2. Power down, connect the verified transistor terminals and common ground, then power the assembly. Check that boot alone does not operate the motor.
3. Send one press. Observe the original five-second LED/motor behavior and confirm that 200 ms is accepted. The firmware reports a pulse, not success of the mechanical action.
4. After the cooldown, send another explicit press and confirm the opposite mode. Confirm that the original S1 still works.

### Results on 2026-10-18

Firmware from commit `60a01ba7d99b88a4fa08504a8c0b6812a3d2c883` was built with local credentials and flashed on COM3. The 4 MB ESP32-C6FH4 and all written flash hashes were verified. Serial startup reached Ready and joined Wi-Fi. The device served the page and script (HTTP 200), rejected unauthenticated status (401), and returned authenticated status with the output released, no fault, and no consumed command sequence. Two status reads showed the same boot and advancing uptime. No press commands were sent by the agent.

The owner then connected PetSafe and reported that remote commands operate the motor and its delayed return, matching the physical button, including operation with USB-C connected. After the proposed 5 V supply test, the owner reported "Well worked. Good results." This is an owner-reported functional result; exact supply measurements, final wiring and RFID-specific performance were not supplied. It does not establish GPIO waveforms through all reset/power-loss conditions or long-term reliability.

The configured binary is `0xd8ec0` bytes with SHA-256 `3b49fab8b8c8c728a364f3113ebed5eae487eb3311939fb6fb547ba66c0b8df0`. It contains credentials and is not published. The sanitized record and original owner reports are in [A01 in the existing register](../../evidence/remaining_work.json); no credentials, token or network identifiers are included there.

### Next: camera integration

Wait for the camera. Use the existing HTTP API or `press.py` for explicit commands; no new firmware or wake hardware is required just to submit a press. The camera/controller must decide when a toggle is appropriate, since the bridge cannot observe the current latch mode or manual presses. A lost response must not trigger an automatic new-sequence retry. First test the camera decision path without actuation, then commission deliberate commands with the owner. No owner action is pending now.

## HTTP API

Use on a trusted local network: **HTTP is not encrypted**. Do not expose port 80 to the internet. All API requests require `Authorization: Bearer <token>`. The HTML/JavaScript contain no token; the page holds the entered token only in memory. There is no CORS support and no action on GET requests.

`GET /api/status` returns:

```json
{
  "firmware": "0.1.0",
  "boot_id": "32-hex-characters",
  "uptime_ms": 10000,
  "next_sequence": 1,
  "last_sequence": 0,
  "command_deadline_ms": 15000,
  "pulse_ms": 200,
  "cooldown_remaining_ms": 0,
  "button_active": false,
  "output_fault": false,
  "door_state": "unknown",
  "power_mode": "always_on"
}
```

`POST /api/press` has **an empty body** and these additional headers, copied from fresh status:

| Header | Value |
|---|---|
| `X-Bridge-Boot` | `boot_id` |
| `X-Bridge-Sequence` | `next_sequence` |
| `X-Bridge-Deadline` | `command_deadline_ms` |

The supplied deadline is five seconds ahead of the status timestamp. The server rejects expired deadlines or deadlines more than ten seconds ahead. Deadlines use ESP uptime, not Unix time; no clock synchronization is required. Use a single coordinating camera service for actuation. Concurrent controllers using the same sequence produce at most one pulse, not two independent commands.

| Response | Meaning |
|---|---|
| 202 `pulse_started` | A 200 ms pulse started; mechanical state remains unknown. |
| 200 `duplicate_no_new_press` | That sequence was already consumed, possibly by a failed attempt; no additional pulse or claim of earlier mechanical success. |
| 400 | Invalid headers or nonempty body; no command accepted. |
| 401 | Missing/wrong token. |
| 409 | Wrong boot, sequence conflict or expired request; no new press. |
| 429 | Cooldown; request is discarded, not queued. |
| 503 `pulse_not_started` | This attempt never reached a HIGH write; `sequence_consumed: true`. Inspect the fault before restarting. |
| 503 `pulse_outcome_uncertain` | A HIGH write was attempted; the pulse may have occurred. `sequence_consumed: true`; do not retry as a fresh toggle. |

**If the response is lost, do not fetch a new sequence and resend automatically.** The pulse may already have happened. A retry of the identical boot/sequence is idempotent while it remains the latest consumed command, including after an error. `last_sequence` tracks attempts, not successful pulses. The status page and client inhibit presses on `output_fault`. Across reboot there is no authoritative outcome or latch state; observe the flap before deciding on another toggle.

The included client uses only Python's standard library:

```powershell
python press.py http://192.168.1.50 --status
python press.py http://192.168.1.50
```

It prompts privately for the token, or reads `PETSAFE_BRIDGE_TOKEN` from the process environment. The second command performs one explicit toggle attempt, never an automatic retry. A camera service can import `press()` from `press.py`; deciding **whether** to toggle and determining the flap's actual mode remain the service's responsibility.

## Verification

Host tests compile and execute the same C policy and output-driver files, with mocked GPIO/GPTimer calls for the latter. Python tests cover configuration and the client; Node tests exercise the shipped web script. These tests cannot establish voltage levels, actual pulse duration or RF/battery performance.

```powershell
python tests/run_tests.py --cc '../../.cache/firmware-test-tools/ziglang/zig.exe'
```

The command above uses the local Zig 0.13.0 host compiler installed under the ignored repository cache. Any suitable host C compiler can be supplied with `--cc`; on Linux, `python tests/run_tests.py --cc cc` uses the system compiler. Python 3 and Node.js are also required.

Validation on 2026-10-18 from clean checkouts of the reviewed fixes: both unconfigured (`0x239c0` bytes) and configured (`0xd8f60` bytes) ESP32-C6 builds passed with ESP-IDF v6.0.2. The configured build used temporary dummy credentials, subsequently removed, and was not flashed. The policy tests, 13 output/failure/interleaving scenarios, six Python tests and web-script tests passed. Tests execute the production reserve-before-driver transaction, including retries after failed assertion, immediate alarm delivery and retention of the pending release when a LOW write fails. The configured ELF places the release callback/helper, critical-section functions, GPIO write and timer-stop functions in IRAM, and active/fault state in DRAM.

The existing KiCad 10.0.5 build, review refresh, all 21 repository regressions and measurement-form tests also passed from a clean checkout. All 82 factory endpoint partitions remain unchanged; only the intentional U6A conflict remains in ERC. Imported asset hashes match committed blobs and checkouts with `core.autocrlf` both enabled and disabled. At the time of those clean-checkout checks, browser rendering and operation on the owned board were unchecked and no hardware was flashed or actuated. The later first-flash, HTTP checks and owner functional results are recorded under Commissioning above.

Commissioning-documentation refresh on 2026-10-18: the existing review refresh and all 21 repository regressions, measurement-form tests and firmware host tests passed. Native schematic, model, capacitor estimates and firmware logic are unchanged from merged PR #7. A fresh KiCad 10.0.5 export succeeded, but ERC could not load the locally installed `power.kicad_sym`, producing 38 library warnings in addition to the retained U6A conflict; direct symbol export also failed. The installed power-library SHA-256 (`782ee8920a2bec30ecaf31f824d74ad814c74a81e4c98046a98f8712116fe0e9`) differs from the recorded stock audit. The previous checked native exports/ERC are retained, not replaced by this environment-dependent failed run. No findings were suppressed and no global library/configuration was changed.

Implementation references: [ESP-IDF HTTP server](https://docs.espressif.com/projects/esp-idf/en/v6.0.2/esp32c6/api-reference/protocols/esp_http_server.html), [GPTimer](https://docs.espressif.com/projects/esp-idf/en/v6.0.2/esp32c6/api-reference/peripherals/gptimer.html), [Wi-Fi](https://docs.espressif.com/projects/esp-idf/en/v6.0.2/esp32c6/api-reference/network/esp_wifi.html).
