"""Test whether notifications aber being (not) triggered
around the boeder of the default radius"""

import notify

USER_SETTINGS = [
    {
        "phone": "+49**********",
        "locations": [
            {
                "name": "somewhere",
                "lat": 49.4865268,
                "lon": 8.3892466,
            }
        ],
    }
]

# distance = 70 km
POSITIVE = [
    # icao, callsign, reg, squawk, lat, lon, alt, vrate, track, speed
    ["000000", "180°", "", "", 48.8570018, 8.3892466, 0, 0, 0, 0],
    ["000000", "225°", "", "", 49.0393844, 7.7101991, 0, 0, 45, 0],
    ["000000", "270°", "", "", 49.4865268, 7.4201902, 0, 0, 90, 0],
    ["000000", "315°", "", "", 49.9296215, 7.6977384, 0, 0, 135, 0],
    ["000000", "  0°", "", "", 50.1160518, 8.3892466, 0, 0, 180, 0],
    ["000000", " 45°", "", "", 49.9296215, 9.0807548, 0, 0, 225, 0],
    ["000000", " 90°", "", "", 49.4865268, 9.3583030, 0, 0, 270, 0],
    ["000000", "135°", "", "", 49.0393844, 9.0682941, 0, 0, 315, 0],
]

# distance = 70.001 km
NEGATIVE = [
    # icao, callsign, reg, squawk, lat, lon, alt, vrate, track, speed
    ["000000", "180°", "", "", 48.8569928, 8.3892466, 0, 0, 0, 0],
    ["000000", "225°", "", "", 49.0393780, 7.7101894, 0, 0, 45, 0],
    ["000000", "270°", "", "", 49.4865268, 7.4201764, 0, 0, 90, 0],
    ["000000", "315°", "", "", 49.9296278, 7.6977284, 0, 0, 135, 0],
    ["000000", "  0°", "", "", 50.1160608, 8.3892466, 0, 0, 180, 0],
    ["000000", " 45°", "", "", 49.9296278, 9.0807648, 0, 0, 225, 0],
    ["000000", " 90°", "", "", 49.4865268, 9.3583168, 0, 0, 270, 0],
    ["000000", "135°", "", "", 49.0393780, 9.0683038, 0, 0, 315, 0],
]


def test_positive():
    """Check whether notifications are being sent for all `POSITIVE` traces"""
    notifications = notify.get_notifications(POSITIVE, USER_SETTINGS)
    assert len(notifications) == 8


def test_negative():
    """Check whether no notifications are being sent for `NEGATIVE` traces"""
    notifications = notify.get_notifications(NEGATIVE, USER_SETTINGS)
    assert len(notifications) == 0
