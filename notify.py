#!/usr/bin/env python3

"""Given ADS-B data, send notifications to users if a HEMS is heading
towards one of the user defined destinations within a certain distance.
"""

import argparse
import sys
import os
import json
import re
import subprocess
from gcmath import (
    LatLon,
    calc_bearing,
    calc_distance,
)

TRACK_DEVIATION = 5  # degrees
MAX_DISTANCE = 70  # km


def get_user_settings(path):
    """Return user settings from JSON file"""
    try:
        with open(path, "r", encoding="utf-8") as settings:
            return json.load(settings)
    except FileNotFoundError:
        pass  # for now...
    except json.JSONDecodeError as ex:
        print(f"{ex}:\n{settings}", file=sys.stderr)

    return []


def format_flight_params(alt: float, vrate: float, distance: float, speed: float):
    """Format flight parameters for the notification to be sent"""
    if int == type(alt):
        result = f"alt {float(alt) * 0.3048:.0f}m"
    elif float == type(alt):
        result = f"alt {alt * 0.3048:.0f}m"
    elif str == type(alt):
        result = f"alt {alt}"
    else:
        result = ""

    if len(result):
        if int == type(vrate):
            result += f"{float(vrate) * 0.3048:+.0f}"
        elif float == type(vrate):
            result += f"{vrate * 0.3048:+.0f}"

    if len(result):
        result += ", "

    result += f"dist {distance:.0f}km"

    if int == type(speed) or str == type(speed):
        speed = float(speed)

    if float == type(speed) and speed:
        speed = speed * 1.852
        eta = distance / speed * 60
        mins = int(eta)
        eta -= mins
        eta *= 60
        secs = int(eta)
        eta = f"eta {mins:02d}:{secs:02d} min"
        result += f", speed {speed:.0f}km/h eta {eta}"

    return result


def get_notifications(data: list[list], settings: list[dict]) -> list[dict]:
    """Iterate over adsb data to determine whether HEMS are heading towards
    user locations by calculating bearing and distance for each combination.
    Return a list of notifications"""

    # pylint: disable=too-many-locals
    # pylint: disable=too-many-nested-blocks

    notifications = []

    try:
        for state in data:
            # squawk is currently not needed, -> _
            icao, callsign, reg, _, lat, lon, alt, vrate, track, speed = state

            if track is not None:
                if alt is None:
                    alt = "unknown"

                if alt != "ground":
                    for user in settings:
                        receipient, locations = user["phone"], user["locations"]

                        for loc in locations:
                            location, pos = loc["name"], LatLon(loc["lat"], loc["lon"])

                            bearing = calc_bearing(LatLon(lat, lon), pos)

                            if abs(bearing - track) <= TRACK_DEVIATION:
                                dist = calc_distance(LatLon(lat, lon), pos)

                                if dist < MAX_DISTANCE:
                                    params = format_flight_params(
                                        alt, vrate, dist, speed
                                    )

                                    callsign = (
                                        re.sub(" *$", " ", callsign) if callsign else ""
                                    )

                                    message = (
                                        f"{callsign}{reg}\n"
                                        f"{location}\n"
                                        f"{params}\n"
                                        f"https://globe.adsbexchange.com/?icao={icao}"
                                    )

                                    notifications.append(
                                        {
                                            "receipient": receipient,
                                            "message": message,
                                        }
                                    )

    except json.JSONDecodeError as ex:
        print(f"{ex}:\n{data}", file=sys.stderr)

    return notifications


if __name__ == "__main__":
    user_settings = get_user_settings(os.path.dirname(__file__) + "/notify.json")

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--stdout", action="store_true")

    args, leftover = parser.parse_known_args()

    for filename in leftover:
        try:
            with open(filename, "r", encoding="utf-8") as file:
                adsb = json.load(file)
                user_notifications = get_notifications(adsb["states"], user_settings)

                if args.stdout:
                    for n in user_notifications:
                        print(f"*** {n['receipient']} ***\n[{n['message']}]\n")
                else:
                    for n in user_notifications:
                        subprocess.call(
                            ["signal-cli", "send", "-m", n["message"], n["receipient"]],
                            stdout=subprocess.DEVNULL,
                            timeout=15,
                        )

        except FileNotFoundError as exception:
            print(f"{exception}:\n{filename}", file=sys.stderr)
