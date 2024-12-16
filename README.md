# Volvo2Mqtt
![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports i386 Architecture][i386-shield]
<br>
![Project Maintenance][maintenance-shield]
[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]

This component establishes a connection between the newer AAOS Volvo cars and Home Assistant via MQTT.<br>
Maybe this component works also with other Volvo cars. Please try out the native Volvo [integration](https://www.home-assistant.io/integrations/volvooncall/) before using this component! If the native component doesn't work for your car, try this mqtt bridge.
<p>

Home Assistant thread can be found [here](https://community.home-assistant.io/t/volvo2mqtt-connect-your-aaos-volvo/585699).

<b>Important note: The Volvo api currently ONLY works in these [countries](https://developer.volvocars.com/terms-and-conditions/apis-supported-locations/)</b>

If you like my work:<br>
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/U7U8MFXCF)

## Confirmed working with
- EX30 BEV (2024)
- XC40 BEV (2024)
- XC40 BEV (2023)
- XC40 BEV (2022)
- XC40 PHEV (2021)
- V60 T8 PHEV (2023)
- V60 T6 PHEV (2025)
- C40 BEV (2023)
- C40 BEV (2022)
- C40 BEV (2024)
- XC90 T8 PHEV (2023)
- XC60 PHEV (2024)
- XC60 PHEV (2023)
- XC60 PHEV (2022)
- XC60 B5 Mildhybrid (2023)
- XC90 PHEV T8 (2023)
- XC90 PHEV T8 (2024)
- XC90 B5 Mildhybrid (2024)
- V90 PHEV T8 (2019)*
- V90 PHEV T6 (2024)
- V90 B5 Mildhybrid (2023)
- EX40 BEV (2025)

*only partly working

Please let me know if your car works with this addon so I can expand the list!<br>


## Supported features
- Lock/unlock car
- Start/stop climate
- Sensor "Battery Charge Level"
- Sensor "Battery Capacity"
- Sensor "Electric Range"
- Sensor "Charging System Status"
- Sensor "Charging Connection Status"
- Sensor "Estimated Charging Finish Time"
- Sensor "Door Lock Status (All doors, tank lid, and engine hood)"
- Sensor "Window Lock Status (All windows and sunroof - Thanks to @navet)"
- Sensor "Engine Status"
- Sensor "Odometer"
- Sensor "Tire Status"
- Sensor "Fuel Status"
- Sensor "Average Fuel Consumption"
- Sensor "Average Speed"
- Sensor "Distance to Empty"
- Sensor "Hours to Service"
- Sensor "Distance to Service"
- Sensor "Months to Service"
- Sensor "Service warning status"
- Sensor "Service warning trigger"
- Car Device Tracker
- Multiple cars

NOTE: Energy status currently available only for cars in the Europe / Middle East / Africa regions. [source](https://developer.volvocars.com/apis/energy/v1/overview/#availability)

## OTP Authentication

As of version <b>v1.9.1</b>, this addon includes improvements to the OTP authentication flow, giving you better control through Home Assistant. 
The authentication process works as follows:

1. Setup volvo2Mqtt, either via Docker, or via HA addon (take a look at the "Setup" section below)
2. Fill in your settings and start volvo2Mqtt
3. In Home Assistant, you'll find two entities:
   - `text.volvo_otp`: For entering the OTP code
   - `button.request_otp`: For requesting a new OTP when needed

To authenticate:
1. Press the "Request OTP" button in Home Assistant
2. Check your email for the OTP code
3. Enter the code in the `text.volvo_otp` entity and press Enter
4. The system will verify your code

If verification fails:
1. Press the "Request OTP" button again to start a new authentication attempt
2. Enter the new OTP code when received

Recent improvements in v1.9.1:
- Removed automatic retries for better control over the authentication process
- Added "Request OTP" button for explicit OTP requests
- Improved error handling and feedback
- OTP codes are now cleared after each verification attempt

Note: Authentication only needs to be done when updating or when explicitly requested, not when restarting the container.

## Setup
<b>Docker:</b>

Just install this addon with the following command.
Please note to fill in your settings inside the environment variables.

`docker run -d --pull=always -e CONF_updateInterval=300 -e CONF_babelLocale='de' -e CONF_mqtt='@json {"broker": "", "username": "", "password": "", "port": 1883}' -e CONF_volvoData='@json {"username": "", "password": "", "vin": "", "vccapikey": ["key1", "key2"]}' -e TZ='Europe/Berlin' --name volvo2mqtt ghcr.io/dielee/volvo2mqtt:latest`

<b>HA Add-On:</b><br>

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FDielee%2Fvolvo2mqtt)

Here is what every option means:

| Environment Variable Name |   Type    | Json Option                           |   Default    | Description                                                     |
| ------------------------- | :-------: | :-----------------------------------: | :----------: | --------------------------------------------------------------- |
| `CONF_updateInterval`     | `int`     |                                       | **required** | Update intervall in seconds.                                     |
| `CONF_babelLocale`        | `string`  |                                       | **required** | Select your country from this [list](https://www.ibm.com/docs/en/radfws/9.7?topic=overview-locales-code-pages-supported). "Locale name" is the column you need!                                        |
| `CONF_mqtt`               | `json`    | `broker`                              | **required** | Your MQTT Broker IP. Eg. 192.168.0.5.
| `CONF_mqtt`               | `json`    | `port`                                | 1883         | Your MQTT Broker Port. If no value is given, port 1883 will be used.  |
| `CONF_mqtt`               | `json`    | `username`                            | optional     | MQTT Username for your broker.
| `CONF_mqtt`               | `json`    | `password`                            | optional     | MQTT Password for your broker.
| `CONF_volvoData`          | `json`    | `username`                            | **required** | Normally your email address to login into the Volvo App.
| `CONF_volvoData`          | `json`    | `password`                            | **required** | Your password to login into the Volvo App.
| `CONF_volvoData`          | `json`    | `vin`                                 | optional     | A single VIN like "VIN1" or a list of VINs like "["VIN1", "VIN2"]". Leave this empty if you don't know your VIN. The addon will use every car that is tied to your account.
| `CONF_volvoData`          | `json`    | `vccapikey`                           | **required** | VCCAPIKEY linked with your volvo developer account. Get your Vccapi key from [here](https://developer.volvocars.com/account/). <b>Starting version 1.8.0, it is possible to define multiple keys, like this: `["vccapikey1", "vccapikey2", "vccapikey3", "etc..."]`</b>
| `CONF_debug`              | `string`  |                                       | optional     | Debug option (true/false). Normally you don't need this. |
| `TZ`                      | `string`  |                                       | **required** | Container timezone eg "Europe/Berlin" from [here](https://docs.diladele.com/docker/timezones.html)|


[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
[releases]: https://github.com/Dielee/volvo2mqtt/releases
[releases-shield]: https://img.shields.io/github/release/Dielee/volvo2mqtt.svg
[maintenance-shield]: https://img.shields.io/maintenance/yes/2024.svg
[commits-shield]: https://img.shields.io/github/commit-activity/y/Dielee/volvo2mqtt.svg
[commits]: https://github.com/Dielee/volvo2mqtt/commits/main
