"""Create JSON test file for testing notifications based on distance"""
import json
from gcmath import LatLon, travel

if "__main__" == __name__:
    bearings = [
        0,
        30,
        45,
        60,
        90,
        120,
        135,
        150,
        180,
        210,
        225,
        240,
        270,
        300,
        315,
        330,
        360,
    ]

    bgu = LatLon(49.4865293, 8.3892454)

    adsb = {"states": []}

    for distance in [69.999, 70.001]:
        for bearing in bearings:
            src = travel(bgu, distance, bearing + 180.0)

            adsb["states"] += [
                [
                    "",
                    "",
                    "",
                    "0020" if distance <= 70.0 else "7000",
                    src.lat,
                    src.lon,
                    0,
                    0,
                    bearing,
                    0,
                ]
            ]

    print(json.dumps(adsb, indent=4))
