"""Create JSON test file for testing the bearing vs track calculation.
As the bearing constantly changes along the way, we cannot simply travel in the
opposite direction by adding 180 degrees. Instead, find the source locations for
different bearings by using this as a starting point and travelling forward,
adjusting the diff until the bearing is close enough.
"""

import argparse
import json
import os
import subprocess
from math import radians, sin, cos
from pathlib import Path
from gcmath import LatLon, calc_bearing, travel


def create_protractor_image(filename: Path, cx: int, cy: int):
    """Create protractor-like base image to draw track/bearing vectors upon"""

    if not filename.exists():
        cmdline = [
            # fmt: off
            "magick",
            "-size", f"{cx}x{cy}",
            "xc:transparent",
            "-alpha", "set",
            "-background", "none",
            "-fill", "none",
            "-stroke", "gray",
            "(",
                "xc:transparent",
            # fmt: on
        ]

        for a in range(0, 360):
            a = radians(a)
            x = round(cx / 2 + cy / 2 * sin(a))
            y = round(cy / 2 - cy / 2 * cos(a))

            cmdline += [
                # fmt: off
                "-draw", f" line {cy / 2},{cy / 2} {x},{y}",
                # fmt: on
            ]

        cmdline += [
            # fmt: off
            ")",
            "(",
                # Crosshair
                "xc:transparent",
                "-stroke", "black",
                "-draw", f"line 0,{cy / 2} {cx},{cy / 2}",
                "-draw", f"line {cx / 2},0 {cx / 2},{cy}",
            ")",
            "(",
                # Legend line "track"
                "xc:transparent",
                "-stroke", "blue",
                "-fill", "blue",
                "-draw", "line 15,15 50,15",
                # Legend line "bearing"
                "-stroke", "blue",
                "-fill", "none",
                "-draw", "stroke-dasharray 5 5 path \"M 15,30 L 50,30\"",
            ")",
            "(",
                # legend text
                "xc:transparent",
                 "-font", "Arial",
                "-pointsize", "16",
                "-strokewidth", "1",
                "-stroke", "none",
                "-fill", "blue",
                "-draw", "text 60,20 'track'",
                "-draw", "text 60,35 'bearing -> bgu'",
            ")",
            "-layers", "flatten",
            filename,
            # fmt: on
        ]

        subprocess.run(cmdline, check=True)


# pylint: disable=too-many-arguments,redefined-outer-name
def create_test_image(
    filename: Path, grid: Path, cx: int, cy: int, track: int, bearing: int
):
    """Create image with track/bearing based on protractor, illustrating the
    test cases. When track and bearing are <= 5 degrees apart, notifications
    shall be sent, and the drawn vectors are drawn in green, otherwise red."""

    t = radians(track)
    tx = round(cx / 2 + cy / 2 * sin(t))
    ty = round(cy / 2 - cy / 2 * cos(t))

    b = radians(bearing)
    bx = round(cx / 2 + cy / 2 * sin(b))
    by = round(cy / 2 - cy / 2 * cos(b))

    subprocess.run(
        [
            # fmt: off
            "magick",
            "-size", f"{cx}x{cy}",
            "xc:transparent",
            grid,
            "-alpha", "set",
            "-background", "none",
            "-fill", "none",
            "-stroke", "green" if abs(deviation) <= 5 else "red",
            "(",
                "xc:transparent",
                "-draw", f"line {cx / 2},{cy / 2} {tx},{ty}",
                "-draw", f"stroke-dasharray 5 5 path \"M {cx / 2},{cx / 2} L {bx},{by}\"",
            ")",
            "-layers", "flatten",
            filename,
            # fmt: on
        ],
        check=True,
    )


if "__main__" == __name__:

    scriptdir = Path(__file__).parent

    CX = 600
    CY = 600

    vectors = [
        # track, bearing
        [0, 354],
        [0, 355],
        [0, 0],
        [0, 5],
        [0, 6],
        [1, 355],
        [1, 356],
        [1, 1],
        [1, 6],
        [1, 7],
        [89, 83],
        [89, 84],
        [89, 89],
        [89, 94],
        [89, 95],
        [90, 84],
        [90, 85],
        [90, 90],
        [90, 95],
        [90, 96],
        [91, 85],
        [91, 86],
        [91, 91],
        [91, 96],
        [91, 97],
        [179, 173],
        [179, 174],
        [179, 179],
        [179, 184],
        [179, 185],
        [180, 174],
        [180, 175],
        [180, 180],
        [180, 185],
        [180, 186],
        [181, 175],
        [181, 176],
        [181, 181],
        [181, 186],
        [181, 187],
        [269, 263],
        [269, 264],
        [269, 269],
        [269, 274],
        [269, 275],
        [270, 264],
        [270, 265],
        [270, 270],
        [270, 275],
        [270, 276],
        [271, 265],
        [271, 266],
        [271, 271],
        [271, 276],
        [271, 277],
        [359, 353],
        [359, 354],
        [359, 359],
        [359, 4],
        [359, 5],
    ]

    bgu = LatLon(49.4865293, 8.3892454)

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-d",
        "--distance",
        type=float,
        default=70.0,
    )

    parser.add_argument(
        "-f",
        "--format",
        choices=["csv", "json"],
        default="json",
        help=(
            "json formatted according to hems-data, "
            "csv formatted to be usable as input to https://www.gpsvisualizer.com/"
        ),
    )

    parser.add_argument(
        "-i",
        "--images",
        action="store_true",
        help=(
            "Create images at --imagedir=, illustrating the "
            "track/bearing vectors in the JSON output"
        ),
    )

    parser.add_argument(
        "--imagedir",
        type=Path,
        default=Path(f"{scriptdir}/img/bearing"),
        help="Create images at IMAGEDIR",
    )

    args = parser.parse_args()

    if args.images:

        if not Path(args.imagedir).exists():
            os.mkdir(args.imagedir)

        create_protractor_image(Path(f"{args.imagedir}/protractor.png"), CX, CY)

    # CSV usable for https://www.gpsvisualizer.com/map_input?form=google
    if "csv" == args.format:
        print("name,latitude,longitude")

    adsb = {"states": []}

    for track, bearing in vectors:
        # Deviation betweeen `track` and `bearing` to BGU
        deviation = bearing - track

        if deviation > 180.0:
            deviation -= 360.0

        if deviation < -180.0:
            deviation += 360.0

        if args.images:
            create_test_image(
                Path(f"{args.imagedir}/{track} {bearing}.png"),
                Path(f"{args.imagedir}/protractor.png"),
                CX,
                CY,
                track,
                bearing,
            )

        reverse = bearing
        # pylint thinks `diff` is contant...
        # pylint: disable=invalid-name
        diff = 180.0

        while abs(diff) > 1.0e-6:
            reverse -= diff
            reverse %= 360.0

            src = travel(bgu, args.distance, reverse)
            # bearing back from `src` to BGU
            forward = calc_bearing(src, bgu)

            diff = forward - bearing

            # `forward` has to be on the side of `track` to stay within `deviation`
            # If `diff` is OK, adding 360 will not exit the loop,
            # but still get the same `reverse` basically
            if (
                deviation > 0
                and forward > bearing
                or deviation < 0
                and forward < bearing
            ):
                diff += 360.0

        if "csv" == args.format:
            print(f"{bearing},{src.lat},{src.lon}")
        else:
            adsb["states"] += [
                [
                    f"bearing={bearing}",
                    " ",
                    " ",
                    "0020" if abs(deviation) <= 5.0 else "7000",
                    src.lat,
                    src.lon,
                    0,
                    0,
                    track,
                    0,
                ]
            ]

    if "json" == args.format:
        print(json.dumps(adsb, indent=4))
