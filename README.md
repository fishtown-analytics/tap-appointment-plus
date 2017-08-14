# tap-appointment-plus

Build: [![CircleCI](https://circleci.com/gh/fishtown-analytics/tap-appointment-plus.svg?style=svg&circle-token=69be301f8d0e7b10cb5965f223912eaf8cd72755)](https://circleci.com/gh/fishtown-analytics/tap-appointment-plus)

Author: Connor McArthur (connor@fishtownanalytics.com)

This is a [Singer](https://singer.io) tap that produces JSON-formatted data following
the [Singer spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:
- Pulls raw data from Appointment Plus's API
- Extracts the following resources:
  - Appointments
  - Coupons
  - Custom Fields
  - Customers
  - Customer Packages
  - Events
  - Locations
  - Packages
  - Payment Types
  - Rooms
  - Services
  - Staff
- Outputs the schema for each resource
- Incrementally pulls data based on the input state

## Quick start

1. Install

    ```bash
    > git clone git@github.com:fishtown-analytics/tap-appointment-plus.git
    > cd tap-appointment-plus
    > pip install .
    ```

2. Get credentials from Appointment Plus:

    You'll need:

    - Your site id (looks like `appointplus123/4`)
    - An Appointment Plus API Key

3. Create the config file.

    There is a template you can use at `config.json.example`, just copy it to `config.json`
    in the repo root and insert your credentials.

    - `site_id`, your Appointment Plus site id.
    - `api_key`, your Appointment Plus API Key.
    - `start_date`, the date from which you want to sync data, in the format `2017-03-10T00:00:00Z`.
    - `user_agent`, the user agent to send to Appointment Plus (replace with your email address)

4. Run the application.

   ```bash
   tap-appointment-plus --config config.json
   ```

---

Copyright &copy; 2017 Fishtown Analytics
