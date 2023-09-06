#!/usr/bin/env python3

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
    try:
        with open(path, "r", encoding="utf-8") as settings:
            return json.load(settings)
    except FileNotFoundError:
        pass  # for now...
    except Exception as ex:
        print(ex, file=sys.stderr)

    return []


def format_flight_params(alt: float, vrate: float, distance: float, speed: float):
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


if __name__ == "__main__":
    user_settings = get_user_settings(os.path.dirname(__file__) + "/notify.json")

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--stdout", action="store_true")

    args, leftover = parser.parse_known_args()

    for filename in leftover:
        try:
            with open(filename, "r", encoding="utf-8") as file:
                adsb = json.load(file)

                for state in adsb["states"]:
                    (
                        icao,
                        callsign,
                        reg,
                        squawk,
                        lat,
                        lon,
                        alt,
                        vrate,
                        track,
                        speed,
                    ) = state

                    if track is not None:
                        if alt is None:
                            alt = "unknown"

                        if alt != "ground":
                            for user in user_settings:
                                receipient, locations = user["phone"], user["locations"]

                                for loc in locations:
                                    location, pos = loc["name"], LatLon(
                                        loc["lat"], loc["lon"]
                                    )

                                    bearing = calc_bearing(LatLon(lat, lon), pos)

                                    if abs(bearing - track) <= TRACK_DEVIATION:
                                        dist = calc_distance(LatLon(lat, lon), pos)

                                        if dist < MAX_DISTANCE:
                                            params = format_flight_params(
                                                alt, vrate, dist, speed
                                            )

                                            callsign = (
                                                re.sub(" *$", " ", callsign)
                                                if callsign
                                                else ""
                                            )

                                            message = (
                                                f"{callsign}{reg}\n"
                                                f"{location}\n"
                                                f"{params}\n"
                                                f"https://globe.adsbexchange.com/?icao={icao}"
                                            )

                                            if args.stdout:
                                                print(f"{message}\n")
                                            else:
                                                subprocess.call(
                                                    [
                                                        "signal-cli",
                                                        "send",
                                                        "-m",
                                                        message,
                                                        receipient,
                                                    ],
                                                    stdout=subprocess.DEVNULL,
                                                    timeout=15,
                                                )
        except FileNotFoundError as exception:
            print(exception, file=sys.stderr)
        except Exception as exception:
            print(exception, file=sys.stderr)

            if adsb:
                print(adsb, file=sys.stderr)
