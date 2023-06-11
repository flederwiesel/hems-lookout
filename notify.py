#!/usr/bin/env python3

import argparse
import sys
import os
import json
import math
import re
import subprocess
from dataclasses import dataclass
from gcmath import (
    LatLon,
    bearing,
    distance,
)

TRACK_DEVIATION = 5 # degrees
MAX_DISTANCE = 70 # km

def getUserLocations(path):
    try:
        with open(path, "r") as file:
            j = json.load(file)

            return j["notifications"]
    except FileNotFoundError:
        pass # for now...
    except Exception as e:
        print(e, file=sys.stderr)

def formatFlightParams(alt: float,
                       vrate: float,
                       distance: float,
                       speed: float):
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
        min = int(eta)
        eta -= min
        eta *= 60
        sec = int(eta)
        eta = f"eta {min:02d}:{sec:02d} min"
        result += f", speed {speed:.0f}km/h eta {eta}"

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--stdout", action='store_true')

    args, leftover = parser.parse_known_args()

    for file in leftover:
        try:
            notifications = getUserLocations(os.path.dirname(__file__) + "/notify.json")

            if notifications:
                with open(file, 'r') as f:
                    j = json.load(f)

                    for s in j["states"]:
                        icao, callsign, reg, squawk, lat, lon, alt, vrate, track, speed = s

                        if track is not None:
                            if alt is None:
                                alt = "unknown"

                            if alt != "ground":

                                for n in notifications:
                                    phone, locations = n["phone"], n["locations"]

                                    for l in locations:
                                        location, pos = l["name"], LatLon(l["lat"], l["lon"])

                                        b = bearing(LatLon(lat, lon), pos)

                                        if abs(b - track) <= TRACK_DEVIATION:
                                            d = distance(LatLon(lat, lon), pos)

                                            if d < MAX_DISTANCE:
                                                params = formatFlightParams(alt, vrate, d, speed)

                                                callsign = re.sub(" *$", " ", callsign) if callsign else ""

                                                message = f"{callsign}{reg}\n" \
                                                    f"{location}\n" \
                                                    f"{params}\n" \
                                                    f"https://globe.adsbexchange.com/?icao={icao}"

                                                if args.stdout:
                                                    print(f"{message}\n")
                                                else:
                                                    subprocess.call([
                                                            "signal-cli", "send", "-m", message, phone
                                                        ],
                                                        stdout=subprocess.DEVNULL,
                                                        timeout=15
                                                    )
        except FileNotFoundError as e:
            print(e, file=sys.stderr)
        except Exception as e:
            print(e, file=sys.stderr)

            if j:
                print(j, file=sys.stderr)
