# MyWaterToronto Integration for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

![logo](logo.png)

**Disclaimer**
This is not an official integration from or supported by the City of Toronto

**Introduciton**
This a _custom component_ for [Home Assistant](https://www.home-assistant.io/). It reads water meter data from the City of Toronto [MyWaterToronto service](https://www.toronto.ca/services-payments/water-environment/how-to-use-less-water/mywatertoronto/).

This integration will create a device for your water meter with several `sensor` entities for various water consumption periods and the date of first and last reading.

**Notes:**
It appears that the City of Toronto only reads the meter every 24-48 hours.  While there is a sensor for Daily usage, this sensor is not accurate.

## Installation

This Integration can be installed in two ways:

**HACS Installation**

Add the following to the Custom Repository under `Settings` in HACS:

`davecpearce/hacs-mywatertoronto` and choose `Integration` as the Category

**Manual Installation**

1. Use Git to clone the repo to a local directory by entering <br/>`git clone https://github.com/davecpearce/hacs-mywatertoronto.git`
1. If you don't already have a `custom_components` directory in your Home Assistant config directory, create it.
3. Copy or move the `mywatertoronto` folder from `hacs-mywatertoronto/custom_components` you cloned from step 1 to the  `custom_components` folder in your Home Assistant `config` folder.

## Track Updates

If installed via HACS, updates are flagged automatically. Otherwise, you will have to manually update as described in the manual installation steps above.

## Configuration

There is a config flow for this integration. After installing the custom component:

1. Go to **Configuration**->**Integrations**
2. Click **+ ADD INTEGRATION** to setup a new integration
3. Search for **MyWaterToronto** and click on it
4. You will be guided through the rest of the setup process via the config flow
   - You will have to provide information from your City of Toronto Utility bill such as Account Number, Client Number, Last Name, Postal Code and Last Payment Method from the upper right hand corner of your bill.

## Available Sensors

| Name                       | Description                                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------- |
| First Read Date            | The first available read date from the meter (Diagnostic).                                              |
| Last Read Date             | The last read date from the meter (Diagnostic).                                                       |
| Total Usage                | The total water usage from the First Read Date.                                                         |
| Daily Usage                | The water usage for each day\*.                                                                              |
| Week To Date Usage         | The water usage for the current week (starting Monday).                                                 |
| Month To Date Usage        | The water usage for the current month.                                                                      |
| Year To Date Usage         | The water usage for the current year.                                                                       |

\* The Daily Usage sensor will not be accurate as the meter usage updates typically occur every 24-48 hours

[buymecoffee]: https://www.buymeacoffee.com/davepearce
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/davecpearce/hacs-mywatertoronto.svg?style=for-the-badge
[commits]: https://github.com/davecpearce/hacs-mywatertoronto/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/davecpearce/hacs-mywatertoronto.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40davecpearce-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/davecpearce/hacs-mywatertoronto.svg?style=for-the-badge
[releases]: https://github.com/davecpearce/hacs-mywatertoronto/releases
[user_profile]: https://github.com/davecpearce