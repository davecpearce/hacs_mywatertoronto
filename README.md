# MyWaterToronto Integration for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![pre-commit][pre-commit-shield]][pre-commit]
[![Black][black-shield]][black]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

![logo](logo.png)

**Disclaimer**
This is not an official integration from or supported by the City of Toronto

**Introduction**
This a _custom component_ for [Home Assistant](https://www.home-assistant.io/). It reads water meter data from the City of Toronto [MyWaterToronto service](https://www.toronto.ca/services-payments/water-environment/how-to-use-less-water/mywatertoronto/).

This integration will create a device for your water meter with several `sensor` entities for various water consumption periods and the date of first and last reading.

**Notes:**
It appears that the City of Toronto only reads the meter every 24-48 hours. While there is a sensor for Daily usage, this sensor is not accurate.

## Installation

This Integration can be installed in two ways:

**HACS Installation**

Add the following to the Custom Repository under `Settings` in HACS:

`davecpearce/hacs_mywatertoronto` and choose `Integration` as the Category

**Manual Installation**

1. Use Git to clone the repo to a local directory by entering <br/>`git clone https://github.com/davecpearce/hacs_mywatertoronto.git`
1. If you don't already have a `custom_components` directory in your Home Assistant config directory, create it.
1. Copy or move the `mywatertoronto` folder from `hacs_mywatertoronto/custom_components` you cloned from step 1 to the `custom_components` folder in your Home Assistant `config` folder.

## Track Updates

If installed via HACS, updates are flagged automatically. Otherwise, you will have to manually update as described in the manual installation steps above.

## Configuration

There is a config flow for this integration. After installing the custom component:

1. Go to **Configuration**->**Integrations**
2. Click **+ ADD INTEGRATION** to setup a new integration
3. Search for **MyWaterToronto** and click on it
4. You will be guided through the rest of the setup process via the config flow
   - You will have to provide information from your City of Toronto Utility bill located in the upper right-hand corner:
     - Account Number
       - Enter a 9-digit number with leading zeros
     - Client Number
       - Enter the first 9 digits (wuth leading zeros) + hyphen + last two digits (nnnnnnnnn-nn)
     - Last Name
       - The last name of the property owner
     - Postal Code
       - Enter postal code in uoppercase and a space (A1A 1A1)
     - Last Payment Method
       - Select from list based on your last payment:
         - N/A (0)
         - Pre-authorized (1)
         - Mail in cheque (2)
         - In person (3)
         - Bank payment (4)
         - Payment drop box (5)
         - MyToronto Pay (6)
       - Ensure future payment methods do not change otherwise this will need to be updated

At this time, the City of Toronto has not added "MyToronto Pay" as an option to their MyWater Toronto website. If your last payment was made with MyToronto Pay, it has been reported that "In Person" may work. You can confirm this by testing your login on the MyWater Toronto website directly.

If you change your payment method and would prefer to keep your sensor history in Home Assistant, edit the config/.storage/core.config_entries file and search for "mywatertoronto".

Change the "last_payment_method" to the numerical value associated with your payment above.

## Available Sensors

| Name                | Description                                                |
| ------------------- | ---------------------------------------------------------- |
| First Read Date     | The first available read date from the meter (Diagnostic). |
| Last Read Date      | The last read date from the meter (Diagnostic).            |
| Total Usage         | The total water usage from the First Read Date.            |
| Daily Usage         | The water usage for each day\*.                            |
| Week To Date Usage  | The water usage for the current week (starting Monday).    |
| Month To Date Usage | The water usage for the current month.                     |
| Year To Date Usage  | The water usage for the current year.                      |

\* The Daily Usage sensor will not be accurate as the meter usage updates typically occur every 24-48 hours

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Credits

This project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

Code template was mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template

---

[black]: https://github.com/psf/black
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
[buymecoffee]: https://www.buymeacoffee.com/davepearce
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/davecpearce/hacs_mywatertoronto.svg?style=for-the-badge
[commits]: https://github.com/davecpearce/hacs_mywatertoronto/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/davecpearce/hacs_mywatertoronto.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40davecpearce-blue.svg?style=for-the-badge
[pre-commit]: https://github.com/pre-commit/pre-commit
[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/davecpearce/hacs_mywatertoronto.svg?style=for-the-badge
[releases]: https://github.com/davecpearce/hacs_mywatertoronto/releases
[user_profile]: https://github.com/davecpearce
