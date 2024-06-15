#!/usr/bin/env python3

"""Given ADS-B data, send notifications to users if a HEMS is heading
towards one of the user defined destinations within a certain distance.
"""

import argparse
import sys
import json
import os
import re
import subprocess
from pathlib import Path
from gcmath import (
    LatLon,
    calc_bearing,
    calc_distance,
)

TRACK_DEVIATION = 5  # degrees
MAX_DISTANCE = 70  # km


def get_notifications(data: list[list], settings: list[dict]) -> list[dict]:
    """Iterate over adsb data to determine whether HEMS are heading towards
    user locations by calculating bearing and distance for each combination.
    Return a list of notifications"""

    # pylint: disable=redefined-outer-name
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-nested-blocks

    notifications = []

    try:
        for state in data:
            # squawk, vrate and speed are currently not needed, -> _
            icao, callsign, reg, _, lat, lon, alt, _, track, _ = state

            if track is not None:
                if alt is None:
                    alt = "unknown"

                if alt != "ground":
                    for user in settings:
                        receipient, locations = user["phone"], user["locations"]

                        for loc in locations:
                            location, pos = loc["name"], LatLon(loc["lat"], loc["lon"])

                            bearing = calc_bearing(LatLon(lat, lon), pos)
                            deviation = bearing - track
                            # Catch track/bearing wrapping around 0°
                            deviation = (deviation + 180.0) % 360.0 - 180.0

                            if abs(deviation) <= TRACK_DEVIATION:
                                dist = calc_distance(LatLon(lat, lon), pos)

                                if dist <= MAX_DISTANCE:
                                    callsign = (
                                        re.sub(" *$", " ", callsign) if callsign else ""
                                    )

                                    message = (
                                        f"{callsign}{reg}\n"
                                        f"{location}\n"
                                        f"https://globe.adsbexchange.com/?icao={icao}"
                                    )

                                    notifications.append(
                                        {
                                            "receipient": receipient,
                                            "message": message,
                                        }
                                    )

    except ValueError as exception:
        print(f"{exception}: {state}", file=sys.stderr)

    return notifications


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--stdout", action="store_true")

    args, files = parser.parse_known_args()

    try:
        homedir = Path(os.getenv("HOME", os.getenv("USERPROFILE")))
        filename = homedir / "hems-lookout-users.json"

        with open(filename, "r", encoding="utf-8") as file:
            settings = json.load(file)

        for filename in files:
            with open(filename, "r", encoding="utf-8") as file:
                adsb = json.load(file)
                notifications = get_notifications(adsb["states"], settings)

                if args.stdout:
                    if notifications:
                        print(f"=== {filename} ===\n")

                    for notification in notifications:
                        print(
                            f"*** {notification['receipient']} ***\n"
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
                                notification["receipient"],
                            ],
                            stdout=subprocess.DEVNULL,
                            timeout=15,
                        )

    except FileNotFoundError as exception:
        print(f"{exception}", file=sys.stderr)

    except json.JSONDecodeError as exception:
        print(f"'{filename}': {exception}", file=sys.stderr)
