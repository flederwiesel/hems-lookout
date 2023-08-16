#!/usr/bin/env python3

"""Do great circle math"""

# We use a lot of gemetric variables (a, b, c, ...),
# not having a "speakable" meaning...
# pylint: disable=invalid-name

import math
from dataclasses import dataclass

EARTH_RADIUS = 6371.000785  # [km] as of GRS-80


def isclose(a: float, b: float) -> bool:
    """Extend
    (`math.isclose()`)[https://docs.python.org/3/library/math.html#math.isclose]
    by using a fixed `abs_tol`
    """
    return math.isclose(a, b, abs_tol=1e-9)


def deg_to_km(d: float, lat: float = 0.0) -> float:
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
            b = 0.0
        else:
            b = 180.0
    else:
        delta = math.radians(dst.lon - src.lon)
        slat = math.radians(src.lat)
        dlat = math.radians(dst.lat)

        b = math.degrees(
            math.atan2(
                math.sin(delta),
                math.cos(slat) * math.tan(dlat) - math.sin(slat) * math.cos(delta),
            )
        )

    return b + 360.0 if b < 0.0 else b


def distance(src: LatLon, dst: LatLon) -> float:
    """Calculate distance **in km** between two coordinates"""
    C = math.radians(dst.lon - src.lon)
    a = math.radians(src.lat)
    b = math.radians(dst.lat)
    c = math.acos(math.sin(a) * math.sin(b) + math.cos(a) * math.cos(b) * math.cos(C))

    if c < 0:
        c += math.pi

    return c * EARTH_RADIUS


# pylint: disable=too-many-nested-blocks,too-many-branches,too-many-statements


def travel(origin: LatLon, dist: float, bear: float) -> LatLon:
    """
    Calculate the position going from one point in a
    certain bearing for a specified distance.

    Result latitude shall be -90.0 ... 90.0°.
    Result longitude shall be -180.0 ... 180.0°.

    Parameters:
        origin -- starting point: LatLon
        dist   -- distance: km
        bear   -- bearing: °
    """
    pos = LatLon(origin.lat, origin.lon)

    if not isclose(dist, 0.0):
        dist = km_to_rad(dist)

        if isclose(bear, 0.0) or isclose(bear, 180.0):
            dist = math.degrees(dist)

            while dist > 360.0:
                dist -= 360.0

            if isclose(bear, 0.0):
                # Travelling north
                if pos.lat < 90.0:
                    pos.lat = origin.lat + dist

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
                    pos.lat = origin.lat - dist

                    if pos.lat < -270.0:
                        pos.lat += 360.0
                    elif pos.lat < -90.0:
                        pos.lat = -180.0 - pos.lat

                        if pos.lon > 0.0:
                            pos.lon -= 180.0
                        else:
                            pos.lon += 180.0

        elif isclose(bear, 90.0) or isclose(bear, 270.0):
            pos.lat = origin.lat

            if isclose(origin.lat, 90.0) or isclose(origin.lat, -90.0):
                # At the poles, we go nowhere heading east or west...
                pos.lon = origin.lon
            else:
                dist = math.degrees(dist)

                if isclose(bear, 90.0):
                    # Travelling east
                    pos.lon = origin.lon + dist / math.cos(math.radians(origin.lat))
                else:
                    # Travelling west
                    pos.lon = origin.lon - dist / math.cos(math.radians(origin.lat))

                # Let longitude be -179.999... .. 180.0
                while (pos.lon <= -180.0) or isclose(pos.lon, -180.0):
                    pos.lon += 360.0

                while pos.lon > 180.0:
                    pos.lon -= 360.0
        else:
            b = math.radians(90.0 - origin.lat)
            a = math.acos(
                math.cos(b) * math.cos(dist)
                + math.sin(b) * math.sin(dist) * math.cos(math.radians(bear))
            )
            q = math.sin(a) * math.sin(b)

            if isclose(q, 0.0):
                raise ZeroDivisionError

            C = math.acos((math.cos(dist) - math.cos(a) * math.cos(b)) / q)

            pos.lat = 90.0 - math.degrees(a)
            pos.lon = (
                origin.lon - math.degrees(C)
                if bear > 180.0
                else origin.lon + math.degrees(C)
            )

            while pos.lon <= -180.0:
                pos.lon += 360.0

            while pos.lon > 180.0:
                pos.lon -= 360.0

    return pos
