"""Test whether notifications aber being (not) triggered
around the boeder of the default radius"""

from pathlib import Path
import json
import logging
import os
import pytest
import notify
from gcmath import LatLon, calc_distance


BGU = LatLon(49.4865293, 8.3892454)

USER_SETTINGS = [
    {
        "recipient": "fcm_token",
        "locations": [
            {
                "name": "BGU Ludwigshafen",
                "lat": BGU.lat,
                "lon": BGU.lon,
            }
        ],
    }
]


@pytest.fixture(name="adsb_data")
def fixture_adb_from_json(filename):
    """Read ADB-B data from json file"""
    scriptdir = Path(__file__).parent

    with open(scriptdir / filename, "r", encoding="utf-8") as file:
        adsb = json.load(file)

    return adsb["states"]


@pytest.fixture(name="fcm_auth_json")
def fixture_fcm_auth_json(tmp_path):
    """Create file from HEMS_LOOKOUT_FCM_AUTH_STR environment variable, if exists,
    otherwise provide content of HEMS_LOOKOUT_FCM_AUTH.
    """

    credentials = os.getenv("HEMS_LOOKOUT_FCM_AUTH_STR")

    if credentials:
        filename = tmp_path / "hems_lookout_fcm_auth.json"

        with open(filename, "w", encoding="utf-8") as file:
            file.write(credentials)
    else:
        filename = os.getenv("HEMS_LOOKOUT_FCM_AUTH")

    return filename


@pytest.mark.parametrize("filename", ["test_notify_distance.json"])
def test_distance_notifyable(adsb_data):
    """Check whether no notifications are being sent"""

    # Only notifyable states
    adsb_data = [d for d in adsb_data if d[3] == "0020"]

    # Check test sanity
    assert len(adsb_data) == 17
    assert (
        len([d for d in adsb_data if calc_distance(BGU, LatLon(d[4], d[5])) > 70.0])
        == 0
    )

    notifications = notify.get_notifications(adsb_data, USER_SETTINGS)
    assert len(notifications) == 17


@pytest.mark.parametrize("filename", ["test_notify_distance.json"])
def test_distance_non_notifyable(adsb_data):
    """Check whether no notifications are being sent"""

    # Only notifyable states
    adsb_data = [d for d in adsb_data if d[3] == "7000"]

    # Check test sanity
    assert len(adsb_data) == 17
    assert (
        len([d for d in adsb_data if calc_distance(BGU, LatLon(d[4], d[5])) <= 70.0])
        == 0
    )

    notifications = notify.get_notifications(adsb_data, USER_SETTINGS)
    assert len(notifications) == 0


@pytest.mark.parametrize("filename", ["test_notify_bearing.json"])
def test_bearing_notifyable(adsb_data):
    """Check whether notifications are being sent for all"""

    # Only notifyable states
    adsb_data = [d for d in adsb_data if d[3] == "0020"]

    # Check test sanity
    assert len(adsb_data) == 36
    assert (
        len([d for d in adsb_data if calc_distance(BGU, LatLon(d[4], d[5])) > 70.0])
        == 0
    )

    notifications = notify.get_notifications(adsb_data, USER_SETTINGS)
    assert len(notifications) == 36


@pytest.mark.parametrize("filename", ["test_notify_bearing.json"])
def test_bearing_non_notifyable(adsb_data):
    """Check whether no notifications are being sent"""

    # Only non-notifyable states
    adsb_data = [d for d in adsb_data if d[3] == "7000"]

    # Check test sanity
    assert len(adsb_data) == 24
    assert (
        len([d for d in adsb_data if calc_distance(BGU, LatLon(d[4], d[5])) > 70.0])
        == 0
    )

    notifications = notify.get_notifications(adsb_data, USER_SETTINGS)
    assert len(notifications) == 0


def test_fcm_send_no_init(caplog):
    """fcm_send() must report no default firebase app without firebase init"""

    caplog.set_level(logging.ERROR)

    notify.fcm_send(
        "invalid",
        notify.Message(
            reg="D-H???", callsign="CHX666", location="Somewhere", href="https://foo"
        ),
        dry_run=True,
    )

    assert "The default Firebase app does not exist." in caplog.text


def test_fcm_send_invalid_token(fcm_auth_json, caplog):
    """fcm_send() must report INVALID_ARGUMENT with invalid token"""

    assert fcm_auth_json

    caplog.set_level(logging.ERROR)

    notify.fcm_init(fcm_auth_json)
    notify.fcm_send(
        "***invalid***",
        notify.Message(
            reg="D-H???", callsign="CHX666", location="Somewhere", href="https://foo"
        ),
        dry_run=True,
    )

    notify.fcm_terminate()

    assert "INVALID_ARGUMENT: 400 Client Error: Bad Request for url" in caplog.text


def test_fcm_send(fcm_auth_json, caplog):
    """fcm_send() must succeed with this token."""

    assert fcm_auth_json

    caplog.set_level(logging.ERROR)

    notify.fcm_init(fcm_auth_json)
    notify.fcm_send(
        "dJOOeRzHQYGo6wvbmqRgxs:APA91bHs7rWx0_r2yJzEM8Go6ulUMi9yTRt87XQ0i6BufZdrfR6c6VIQPli"
        "wDH_iOC_JQ8lXPAc9o11cO776DMJp7ui9MlosiOuzVRiekJc3NqZTEf5XOBxlKrB21YXT3vjVHdHpgdp1",
        notify.Message(
            reg="D-H???", callsign="CHX666", location="Somewhere", href="https://foo"
        ),
        dry_run=True,
    )

    notify.fcm_terminate()

    assert 0 == len(caplog.text)
