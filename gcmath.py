#!/usr/bin/env python3

"""Do great circle math"""

import math
from dataclasses import dataclass

EARTH_RADIUS = 6371.000785 # [km] as of GRS-80


def isclose(a: float, b: float) -> bool:
    return math.isclose(a, b, abs_tol=1e-9)


def deg_to_km(d: float, lat: float=0.0) -> float:
    """Convert decimal degrees to km, travelling on a WGS-84 surface"""
    if not isclose(lat, 0.0):
        d *= math.cos(math.radians(lat))

    return d * math.pi * EARTH_RADIUS / 180.0


def km_to_deg(d: float) -> float:
    """Convert km to decimal degrees, travelling on a WGS-84 surface"""
    return d / math.pi / EARTH_RADIUS * 180.0


def km_to_rad(d: float) -> float:
    """Convert km to radians, travelling on a WGS-84 surface"""
    return d / EARTH_RADIUS


@dataclass
class LatLon:
    """A simple class holding latitude/longitude"""
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def __repr__(self) -> str:
        return f"({self.lat}, {self.lon})"

    def __eq__(self, other) -> bool:
        return isclose(self.lat, other.lat) and isclose(self.lon, other.lon)


def bearing(src: LatLon, dst: LatLon) -> float:
    """Calculate bearing between two coordinates"""
    if dst.lon == src.lon:
        if dst.lat >= src.lat:
            bearing = 0.0
        else:
            bearing = 180.0
    else:
        delta = math.radians(dst.lon - src.lon);
        slat = math.radians(src.lat);
        dlat = math.radians(dst.lat);

        bearing = math.degrees(
            math.atan2(
                math.sin(delta),
                math.cos(slat) * math.tan(dlat) - math.sin(slat) * math.cos(delta)
            )
        )

    return bearing + 360.0 if bearing < 0.0 else bearing


def distance(src: LatLon, dst: LatLon) -> float:
    """Calculate distance **in km** between two coordinates"""
    C = math.radians(dst.lon - src.lon);
    a = math.radians(src.lat);
    b = math.radians(dst.lat);
    c = math.acos(math.sin(a) * math.sin(b) + math.cos(a) * math.cos(b) * math.cos(C));

    if c < 0:
        c += math.pi;

    return c * EARTH_RADIUS


def travel(origin: LatLon, distance: float, bearing: float) -> LatLon:
    """
    Calculate the position going from on point in a
    certain bearing for a specified distance.

    Result latitude shall be -90.0 ... 90.0°.
    Result longitude shall be -180.0 ... 180.0°.

    Parameters:
        origin   [(lat°, lon°)]
        distance [km]
        bearing  [°]
    """
    pos = LatLon(origin.lat, origin.lon)

    if not isclose(distance, 0.0):

        distance = km_to_rad(distance)

        if isclose(bearing, 0.0) or isclose(bearing, 180.0):

            distance = math.degrees(distance)

            while distance > 360.0:
                distance -= 360.0

            if isclose(bearing, 0.0):
                # Travelling north
                if pos.lat < 90.0:
                    pos.lat = origin.lat + distance

                    if pos.lat > 270.0:
                        pos.lat -= 360.0

                    elif pos.lat > 90.0:
                        pos.lat = 180.0 - pos.lat

                        if pos.lon > 0.0:
                            pos.lon -= 180.0
                        else:
                            pos.lon += 180.0
            else:
                # Travelling south
                if pos.lat > -90.0:
                    pos.lat = origin.lat - distance

                    if pos.lat < -270.0:
                        pos.lat += 360.0
                    elif pos.lat < -90.0:
                        pos.lat = -180.0 - pos.lat

                        if pos.lon > 0.0:
                            pos.lon -= 180.0
                        else:
                            pos.lon += 180.0

        elif isclose(bearing, 90.0) or isclose(bearing, 270.0):

            pos.lat = origin.lat

            if isclose(origin.lat, 90.0) or isclose(origin.lat, -90.0):
                # At the poles, we go nowhere heading east or west...
                pos.lon = origin.lon
            else:
                distance = math.degrees(distance)

                if isclose(bearing, 90.0):
                    # Travelling east
                    pos.lon = origin.lon + distance / math.cos(math.radians(origin.lat))
                else:
                    # Travelling west
                    pos.lon = origin.lon - distance / math.cos(math.radians(origin.lat))

                # Let longitude be -179.999... .. 180.0
                while (pos.lon <= -180.0) or isclose(pos.lon, -180.0):
                    pos.lon += 360.0

                while (pos.lon > 180.0):
                    pos.lon -= 360.0
        else:

            b = math.radians(90.0 - origin.lat)
            a = math.acos(math.cos(b) * math.cos(distance) + math.sin(b) * math.sin(distance) * math.cos(math.radians(bearing)))
            q = math.sin(a) * math.sin(b)

            if isclose(q, 0.0):
                raise ZeroDivisionError
            else:
                C = math.acos((math.cos(distance) - math.cos(a) * math.cos(b)) / q)

            pos.lat = 90.0 - math.degrees(a)
            pos.lon = origin.lon - math.degrees(C) if bearing > 180.0 else origin.lon + math.degrees(C)

            while pos.lon <= -180.0:
                pos.lon += 360.0

            while pos.lon > 180.0:
                pos.lon -= 360.0

    return pos
