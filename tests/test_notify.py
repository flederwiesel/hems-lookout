"""Test whether notifications aber being (not) triggered
around the boeder of the default radius"""

from pathlib import Path
import json
import pytest
import notify
from gcmath import LatLon, calc_distance


BGU = LatLon(49.4865293, 8.3892454)

USER_SETTINGS = [
    {
        "phone": "+49**********",
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
