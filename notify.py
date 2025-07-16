#!/usr/bin/env python3

"""Given ADS-B data, send notifications to users if a HEMS is heading
towards one of the user defined destinations within a certain distance.
"""

import argparse
import os
import json
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging  # pylint: disable=unused-import
from gcmath import (
    LatLon,
    calc_bearing,
    calc_distance,
)

TRACK_DEVIATION = 5  # degrees
MAX_DISTANCE = 70  # km


class InsufficientData(Exception):
    """Do nothing"""


@dataclass
class AicraftState:
    """Data class to be initialised from dict, as read from data/hems/**.json.
    Raises InsufficientData exception in constructor, if essential values are missing.
    """

    # pylint: disable=too-many-instance-attributes
    def __init__(self, state: list):
        # fmt: off
        (
            # Comments below denote possible different types
            self.icao,      # str
            self.callsign,  # str
            self.reg,       # None|str
            self.squawk,    # None|str
            lat,            # float
            lon,            # float
            self.alt,       # int|str"ground"
            self.vrate,     # None|float
            self.track,     # float
            self.speed,     # float
        ) = state
        # fmt: on

        if not any([self.icao, self.callsign, self.reg]):
            # We want at least _something_ to report...
            raise InsufficientData

        if None in [lat, lon, self.track]:
            # Cannot calculate anything...
            raise InsufficientData

        self.callsign = self.callsign.strip() if self.callsign else ""
        self.reg = self.reg.strip() if self.reg else ""

        # Backup: Report ICAO hex code instead of empty string....
        if not (self.callsign and self.reg):
            self.callsign = self.icao

        self.pos = LatLon(lat, lon)


@dataclass
class Message:
    """Data class to hold notification message data"""

    def __init__(self, **kwargs):
        self.timestamp = datetime.now().isoformat(timespec="seconds")
        self.reg = kwargs["reg"]
        self.callsign = kwargs["callsign"]
        self.location = kwargs["location"]
        self.href = kwargs["href"]

    def __str__(self):
        return (
            # fmt: off
            f"{self.callsign} {self.reg}".strip() + "\n"
            f"{self.location}"
            # fmt: on
        )


def fcm_init(filename: Path) -> None:
    """Initialise messaging app from service accout key data JSON file"""
    firebase_admin.initialize_app(credentials.Certificate(filename))


def fcm_terminate() -> None:
    """Release internal app object. Only for testing."""
    firebase_admin.delete_app(firebase_admin.get_app())


def fcm_send(recipient: str, message: Message, dry_run=False) -> None:
    """Send a notification via Firebase Cloud Messaging"""

    try:
        # https://firebase.google.com/docs/reference/admin/python/firebase_admin.messaging
        wrap = firebase_admin.messaging.Message(
            token=recipient,
            notification=None,
            data=message.__dict__,
        )

        fcmlog.info("? %s", message)
        firebase_admin.messaging.send(wrap, dry_run)
        fcmlog.info("=")

    except firebase_admin.exceptions.NotFoundError:
        msg = f"Token '{recipient}' not found."
        logging.warning(msg)
        fcmlog.warning("! %s", msg)
    except firebase_admin.exceptions.FirebaseError as ex:
        msg = (
            f"{ex.code if ex.code else 'UNKNOWN CODE'}: "
            f"{ex.cause if ex.cause else 'UNKNOWN CAUSE'}: "
            f"{ex.http_response if ex.http_response else ''}"
        )
        logging.error(msg)
        fcmlog.error("! %s", msg)
    # pylint: disable=broad-exception-caught
    except Exception as ex:
        logging.error("%s", ex)
        fcmlog.error("! %s", ex)


def isnotifyable(state: AicraftState, poi: LatLon) -> bool:
    """Determine whether notifications shall be sent for an AicraftState"""
    bearing = calc_bearing(state.pos, poi)
    deviation = bearing - state.track

    # Catch track/bearing wrapping around 0°
    deviation = (deviation + 180.0) % 360.0 - 180.0

    if abs(deviation) <= TRACK_DEVIATION:
        dist = calc_distance(state.pos, poi)

        if dist <= MAX_DISTANCE:
            return True

    return False


def get_notifications(data: list[list], settings: list[dict]) -> list[dict]:
    """Iterate over adsb data to determine whether HEMS are heading towards
    user locations by calculating bearing and distance for each combination.
    Return a list of notifications"""

    # pylint: disable=too-many-nested-blocks

    notifications = []

    for state in data:
        try:
            state = AicraftState(state)

            for user in settings:
                recipient, locations = user["recipient"], user["locations"]

                for loc in locations:
                    location, poi = loc["name"], LatLon(loc["lat"], loc["lon"])

                    if isnotifyable(state, poi):
                        if state.callsign is None and state.reg is None:
                            # class AicraftState makes sure that icao is not None now
                            state.callsign = state.icao

                        # Simply move map to position, if icao is unknown
                        qsa = (
                            f"icao={state.icao}"
                            if state.icao
                            else f"lat={state.pos.lat}&lon={state.pos.lon}"
                        )

                        notifications.append(
                            {
                                "recipient": recipient,
                                "message": Message(
                                    location=location,
                                    callsign=state.callsign,
                                    reg=state.reg,
                                    href=f"https://globe.adsbexchange.com/?{qsa}",
                                ),
                            }
                        )
        except InsufficientData:
            logging.debug("InsufficientData: %s", json.dumps(state))
        except ValueError as exception:
            logging.error("%s: %s", exception, state)

    return notifications


def main():
    """Place Chuck Norris joke here..."""

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--stdout", action="store_true")
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-D", "--dry-run", action="store_true")
    parser.add_argument("--fcm-credentials", type=Path, required=False, default=None)

    args, leftover = parser.parse_known_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        homedir = Path(os.getenv("HOME", os.getenv("USERPROFILE")))
        filename = homedir / "hems-lookout-users.json"

        with open(filename, "r", encoding="utf-8") as file:
            settings = json.load(file)

        if not args.stdout:
            filename = (
                args.fcm_credentials
                if args.fcm_credentials
                else os.getenv(
                    "HEMS_LOOKOUT_FCM_AUTH",
                    default=Path().home() / "hems-lookout-fcm.json",
                )
            )

            fcm_init(filename)

        for filename in leftover:
            with open(filename, "r", encoding="utf-8") as file:
                adsb = json.load(file)
                notifications = get_notifications(adsb["states"], settings)

                if args.stdout:
                    if notifications:
                        print(f"=== {filename} ===\n")

                    for notification in notifications:
                        print(f"*** {notification['recipient']} ***")
                        print(notification["message"])
                else:
                    for notification in notifications:
                        fcm_send(notification["recipient"], notification["message"], args.dry_run)

    except FileNotFoundError as exception:
        logging.error("'%s': %s", filename, exception)

    except json.JSONDecodeError as exception:
        logging.error("'%s': %s", filename, exception)


class FoldLinesFormatter(logging.Formatter):
    """Formatter that folds lines by replacing all newline characters in a log message"""

    def format(self, record: logging.LogRecord) -> str:
        return super().format(record).replace("\n", " ")


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(filename)s(%(lineno)d): %(message)s",
)

handler = logging.FileHandler(Path.home() / "hems-lookout.log")
handler.setFormatter(FoldLinesFormatter(fmt="%(asctime)s %(message)s"))

fcmlog = logging.getLogger("fcmlog")
fcmlog.addHandler(handler)
fcmlog.setLevel(logging.DEBUG)
fcmlog.propagate = False

if __name__ == "__main__":
    main()
