# Slide Local

Home Assistant integration to control Slide devices locally.

## About

Slide Local is a custom Home Assistant integration that controls Slide motorized curtain tracks directly over your local network, without requiring a cloud service. It exposes each curtain as a cover entity with position control, open/close/stop, and a **calibration button** to recalibrate the curtain position.

## Installation

### HACS

1. Ensure [HACS](https://hacs.xyz/) is installed and up to date.
2. Open HACS, select **Custom repositories**, and add `https://github.com/Jeroendg/Slide-Local` as an **Integration**.
3. Search for **Slide Local**, select **Download**, and restart Home Assistant.

### Manual

1. Download the repository source from [GitHub](https://github.com/Jeroendg/Slide-Local/archive/refs/heads/main.zip).
2. Copy the `custom_components/slide_local` directory into your Home Assistant `custom_components/` folder.
3. Restart Home Assistant.

## Configuration

This integration is configured through Home Assistant's **Settings → Devices & Services → Add Integration** flow:

1. Search for **Slide Local**.
2. Enter a name for the device (e.g., "Living Room").
3. Enter the Slide device's IP address.
4. Enter the Slide device ID.
5. Confirm and finish setup.

The integration uses a config flow and does not support YAML configuration.

## Devices

Each Slide hub is represented as a device containing:

- **Cover entities** — One per curtain track, supporting position control (0–100%), open, close, and stop.
- **Calibration button** — One per curtain track. Pressing this button triggers a calibration routine on the physical curtain.

### Calibration Button

The calibration button re-sends the calibration command to the Slide device. Use this when a curtain's position appears out of sync with its actual physical position (e.g., after a power outage or manual move).

> ⚠️ **Warning:** Calibration will move the curtain to its limits. Ensure the curtain track is clear of obstructions before running calibration.

After calibration, the cover entity's position should accurately reflect the physical curtain position.

## Requirements

- A currently supported Home Assistant release
- A Slide device with Local API enabled (firmware updated after August 2023)
- Python package `SlideLocalAPI==0.3.0` (installed automatically by Home Assistant)

## Troubleshooting

- **Cannot connect to Slide:** Verify the IP address is correct and the device is reachable on your LAN. Ensure the Local API is enabled in the Slide's mobile app settings.
- **Cover position wrong after calibration:** Run the calibration button again. If the issue persists, check that the Slide device firmware is up to date.
- **Entity shows unavailable:** The Slide device may be offline or the IP address may have changed. Check your router's DHCP lease table.

## License

This project is licensed under the [GNU General Public License v3 (GPLv3)](LICENSE).

## Repository

[https://github.com/Jeroendg/Slide-Local](https://github.com/Jeroendg/Slide-Local)
