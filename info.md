# MyWaterToronto Integration for Home Assistant

![logo](logo.png)

**Disclaimer**
This is not an official integration from or supported by the City of Toronto

**Introduction**
This a _custom component_ for [Home Assistant](https://www.home-assistant.io/). It reads water meter data from the City of Toronto [MyWaterToronto service](https://www.toronto.ca/services-payments/water-environment/how-to-use-less-water/mywatertoronto/).

This integration will create a device for your water meter with several `sensor` entities for various water consumption periods and the date of first and last reading.

**Notes:**
It appears that the City of Toronto only reads the meter every 24-48 hours. While there is a sensor for Daily usage, this sensor is not accurate.

**HACS Installation**

Add the following to the Custom Repository under `Settings` in HACS:

`davecpearce/hacs_mywatertoronto` and choose `Integration` as the Category

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
       - Select from list baased on your last payment:
         - Pre-authorized
         - Mail in cheque
         - In person
         - Bank payment
         - Payment drop box
       - Ensure future payment methods do not change otherwise this will need to be updated

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
