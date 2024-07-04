# HEMS lookout

[![status](https://github.com/flederwiesel/hems-lookout/actions/workflows/code_checks.yml/badge.svg)](https://github.com/flederwiesel/hems-lookout/actions/workflows/code_checks.yml)

Send notifications whenever a HEMS is heading towards any POI from a customisable list.

Notification messages are made up of callsign, registration and href to
adsbexchange.com map, in addition to the POI name.

Notifications are being sent using
[Firebase Cloud Messaging](https://console.firebase.google.com/project/hems-lookout/overview).
To configure Google Service Accounts and permissions, see the
[Google Cloud Console](https://console.cloud.google.com/iam-admin/serviceaccounts?project=hems-lookout&authuser=0&hl=en).

## Files

* `$HOME/hems-lookout.conf`

    May contain shell variables to be sourced upon start.

* `$HOME/hems-lookout-users.json`

    "Database" containing FCM tokens and associated POIs.

* `query-adsb.sh`

    Retrieve ADS-B data from rapidapi.com and store them in `data/adsb` as xz.
    Filter by squawk and registration regex, save result to `data/hems` as JSON.
    Then call `notify.py` on the latter.

* `notify.py`

    Check json data gathered by `query-adsb.sh` against POIs in `notify.json` and
    send FCM notifications for each match. FCM authentication data is expected
    as service account JSON data in configurable locations.

* `notify.json`

    Define notification settings - multiple POIs per recipient (as FCM tokens).

    ```json
    [
        {
            "recipient": "fcm_token",
            "locations": [
                {
                    "name": "BGU Ludwigshafen",
                    "lat": 49.4865268,
                    "lon": 8.3892466
                },
                {
                    ...
                }
            ]
        }
    ]
    ```

* `gcmath.py`

    Module defining LatLon classs and great circle calculations.

* `deploy.sh`

    Synchronise required files to remote.

* `install.sh`

    Set up Python venv and cronjob.


## Environment

* `RAPIDAPI_KEY_ADSBEXCHANGE`

    Key to authenticate against `https://adsbexchange-com1.p.rapidapi.com/v2`.

* `HEMS_LOOKOUT_FCM_AUTH`

    Specify location of Firebase service account data file required by `notify.py`.

* `HEMS_LOOKOUT_FCM_AUTH_STR`

    For testing, specify Firebase service account data as string. Required by
    `test_notify.py`, to create the service account file from a secret.
