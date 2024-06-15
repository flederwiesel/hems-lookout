#!/usr/bin/env python3

"""Given ADS-B data, send notifications to users if a HEMS is heading
towards one of the user defined destinations within a certain distance.
"""

import argparse
import sys
import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
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

    # pylint: disable=redefined-outer-name
    # pylint: disable=too-many-locals
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
                        message = (
                            f"{state.callsign}"
                            f"{' ' if len(state.callsign) and len(state.reg) else ''}"
                            f"{state.reg}\n"
                            f"{location}\n"
                            f"https://globe.adsbexchange.com/?icao={state.icao}"
                        )

                        notifications.append(
                            {
                                "recipient": recipient,
                                "message": message,
                            }
                        )
        except InsufficientData:
            print("InsufficientData: %s", json.dumps(state))
        except ValueError as exception:
            print(f"{exception}: {state}", file=sys.stderr)

    return notifications


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--stdout", action="store_true")

    args, leftover = parser.parse_known_args()

    try:
        homedir = Path(os.getenv("HOME", os.getenv("USERPROFILE")))
        filename = homedir / "hems-lookout-users.json"

        with open(filename, "r", encoding="utf-8") as file:
            settings = json.load(file)

        for filename in leftover:
            with open(filename, "r", encoding="utf-8") as file:
                adsb = json.load(file)
                notifications = get_notifications(adsb["states"], settings)

                if args.stdout:
                    if notifications:
                        print(f"=== {filename} ===\n")

                    for notification in notifications:
                        print(
                            f"*** {notification['recipient']} ***\n"
                            f"{notification['message']}\n"
                        )
                else:
                    for notification in notifications:
                        subprocess.call(
                            [
                                "signal-cli",
                                "send",
                                "-m",
                                notification["message"],
                                notification["recipient"],
                            ],
                            stdout=subprocess.DEVNULL,
                            timeout=15,
                        )

    except FileNotFoundError as exception:
        print(f"{exception}", file=sys.stderr)

    except json.JSONDecodeError as exception:
        print(f"'{filename}': {exception}", file=sys.stderr)
