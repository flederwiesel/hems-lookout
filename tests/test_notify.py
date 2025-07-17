"""Test whether notifications aber being (not) triggered
around the boeder of the default radius"""

from pathlib import Path
import json
import logging
import os
import pytest
from requests.exceptions import HTTPError
import firebase_admin
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


class MockFirebaseAdmin:
    """A class mocking the essentials of firebase_admin"""

    _DEFAULT_APP_NAME = "[DEFAULT]"

    def __init__(self):
        self.app = None

    def initialize_app(
        self,
        credential=None,  # pylint: disable=unused-argument
        name: str = _DEFAULT_APP_NAME,
    ):
        """Set app name, so messaging.send() can raise, if no initialize_app() called"""
        self.app = name

    def delete_app(self, name=_DEFAULT_APP_NAME):
        """Actually not used, just here for completeness"""
        if self.app == name:
            self.app = None
        else:
            raise ValueError(
                (
                    f"Firebase app named '{name}' is not initialized. Make sure to initialize "
                    "the app by calling initialize_app() with your app name as the "
                    "second argument."
                )
            )

    def get_app(self, name: str = _DEFAULT_APP_NAME):  # pylint: disable=unused-argument
        """Return app name to check whether initialize_app() has been called"""
        return self.app

    class messaging:  # pylint: disable=invalid-name,too-few-public-methods
        """Mock the messaging subclass"""

        @classmethod
        def send(
            cls,
            message: firebase_admin.messaging.Message,
            dry_run: bool = False,  # pylint: disable=unused-argument
            name=None,
        ):
            """Simple send mock, raising if app has not been initialized
            or the token is ***invalid***"""
            app = firebase_admin.get_app()

            if not app:
                if name:
                    raise ValueError(
                        (
                            f"Firebase app named '{name}' does not exist. Make sure to initialize "
                            "the SDK by calling initialize_app() with your app name as the "
                            "second argument."
                        )
                    )
                raise ValueError(
                    "The default Firebase app does not exist. Make sure to initialize "
                    "the SDK by calling initialize_app()."
                )

            if message.token == "***invalid***":
                raise firebase_admin.exceptions.InvalidArgumentError(
                    message="The registration token is not a valid FCM registration token",
                    cause=HTTPError(
                        "400 Client Error: Bad Request for url: https://..."
                    ),
                )

            return "projects/hems-lookout/messages/fake_message_id"


@pytest.fixture(name="mock_firebase_admin")
def fixture_mock_firebase_admin(monkeypatch):
    """Fixture patching firebase_admin to MockFirebaseAdmin()"""
    mock = MockFirebaseAdmin()
    monkeypatch.setattr(firebase_admin, "initialize_app", mock.initialize_app)
    monkeypatch.setattr(firebase_admin, "delete_app", mock.delete_app)
    monkeypatch.setattr(firebase_admin, "get_app", mock.get_app)
    monkeypatch.setattr(firebase_admin.messaging, "send", mock.messaging.send)


@pytest.fixture(name="adsb_data")
def fixture_adsb_from_json(filename):
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


def test_fcm_send_no_init(
    mock_firebase_admin, caplog  # pylint: disable=unused-argument
):
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


def test_fcm_send_invalid_token(
    fcm_auth_json, mock_firebase_admin, caplog  # pylint: disable=unused-argument
):
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


def test_fcm_send(
    fcm_auth_json, mock_firebase_admin, caplog  # pylint: disable=unused-argument
):
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
