"""Test gmath functions"""

# pylint: disable=line-too-long, disable=too-many-statements

from gcmath import (
    LatLon,
    calc_bearing,
    calc_distance,
    travel,
    isclose,
    deg_to_km,
)

def test_travel_nowhere():
    """Going nowhere..."""
    assert travel(LatLon(0.0, 0.0), 0.0, 0.0) == LatLon(0.0, 0.0)
    assert travel(LatLon(0.0, 0.0), 0.0, 90.0) == LatLon(0.0, 0.0)
    assert travel(LatLon(90.0, 0.0), 0.0, 180.0) == LatLon(90.0, 0.0)

def test_travel_north():
    """Along circles of longitude"""
    assert travel(LatLon(-90.0, 0), deg_to_km(  0), 0.0) == LatLon(-90.0,   0.0)
    assert travel(LatLon(-90.0, 0), deg_to_km( 10), 0.0) == LatLon(-80.0,   0.0)
    assert travel(LatLon(-90.0, 0), deg_to_km( 80), 0.0) == LatLon(-10.0,   0.0)
    assert travel(LatLon(-90.0, 0), deg_to_km( 90), 0.0) == LatLon(  0.0,   0.0)
    assert travel(LatLon(-90.0, 0), deg_to_km(100), 0.0) == LatLon( 10.0,   0.0)
    assert travel(LatLon(-90.0, 0), deg_to_km(170), 0.0) == LatLon( 80.0,   0.0)
    assert travel(LatLon(-90.0, 0), deg_to_km(180), 0.0) == LatLon( 90.0,   0.0)
    assert travel(LatLon(-90.0, 0), deg_to_km(190), 0.0) == LatLon( 80.0, 180.0)
    assert travel(LatLon(-90.0, 0), deg_to_km(260), 0.0) == LatLon( 10.0, 180.0)
    assert travel(LatLon(-90.0, 0), deg_to_km(270), 0.0) == LatLon(  0.0, 180.0)
    assert travel(LatLon(-90.0, 0), deg_to_km(280), 0.0) == LatLon(-10.0, 180.0)
    assert travel(LatLon(-90.0, 0), deg_to_km(350), 0.0) == LatLon(-80.0, 180.0)
    assert travel(LatLon(-90.0, 0), deg_to_km(360), 0.0) == LatLon(-90.0, 180.0)
    assert travel(LatLon(-90.0, 0), deg_to_km(370), 0.0) == LatLon(-80.0,   0.0)

    assert travel(LatLon(-80.0, 0), deg_to_km(  0), 0.0) == LatLon(-80.0,   0.0)
    assert travel(LatLon(-80.0, 0), deg_to_km( 10), 0.0) == LatLon(-70.0,   0.0)
    assert travel(LatLon(-80.0, 0), deg_to_km( 80), 0.0) == LatLon(  0.0,   0.0)
    assert travel(LatLon(-80.0, 0), deg_to_km( 90), 0.0) == LatLon( 10.0,   0.0)
    assert travel(LatLon(-80.0, 0), deg_to_km(100), 0.0) == LatLon( 20.0,   0.0)
    assert travel(LatLon(-80.0, 0), deg_to_km(170), 0.0) == LatLon( 90.0,   0.0)
    assert travel(LatLon(-80.0, 0), deg_to_km(180), 0.0) == LatLon( 80.0, 180.0)
    assert travel(LatLon(-80.0, 0), deg_to_km(190), 0.0) == LatLon( 70.0, 180.0)
    assert travel(LatLon(-80.0, 0), deg_to_km(260), 0.0) == LatLon(  0.0, 180.0)
    assert travel(LatLon(-80.0, 0), deg_to_km(270), 0.0) == LatLon(-10.0, 180.0)
    assert travel(LatLon(-80.0, 0), deg_to_km(280), 0.0) == LatLon(-20.0, 180.0)
    assert travel(LatLon(-80.0, 0), deg_to_km(350), 0.0) == LatLon(-90.0, 180.0)
    assert travel(LatLon(-80.0, 0), deg_to_km(360), 0.0) == LatLon(-80.0,   0.0)
    assert travel(LatLon(-80.0, 0), deg_to_km(370), 0.0) == LatLon(-70.0,   0.0)

    assert travel(LatLon(-10.0, 0), deg_to_km(  0), 0.0) == LatLon(-10.0,   0.0)
    assert travel(LatLon(-10.0, 0), deg_to_km( 10), 0.0) == LatLon(  0.0,   0.0)
    assert travel(LatLon(-10.0, 0), deg_to_km( 80), 0.0) == LatLon( 70.0,   0.0)
    assert travel(LatLon(-10.0, 0), deg_to_km( 90), 0.0) == LatLon( 80.0,   0.0)
    assert travel(LatLon(-10.0, 0), deg_to_km(100), 0.0) == LatLon( 90.0,   0.0)
    assert travel(LatLon(-10.0, 0), deg_to_km(170), 0.0) == LatLon( 20.0, 180.0)
    assert travel(LatLon(-10.0, 0), deg_to_km(180), 0.0) == LatLon( 10.0, 180.0)
    assert travel(LatLon(-10.0, 0), deg_to_km(190), 0.0) == LatLon(  0.0, 180.0)
    assert travel(LatLon(-10.0, 0), deg_to_km(260), 0.0) == LatLon(-70.0, 180.0)
    assert travel(LatLon(-10.0, 0), deg_to_km(270), 0.0) == LatLon(-80.0, 180.0)
    assert travel(LatLon(-10.0, 0), deg_to_km(280), 0.0) == LatLon(-90.0, 180.0)
    assert travel(LatLon(-10.0, 0), deg_to_km(350), 0.0) == LatLon(-20.0,   0.0)
    assert travel(LatLon(-10.0, 0), deg_to_km(360), 0.0) == LatLon(-10.0,   0.0)
    assert travel(LatLon(-10.0, 0), deg_to_km(370), 0.0) == LatLon(  0.0,   0.0)

    assert travel(LatLon(0.0, 0), deg_to_km(  0), 0.0) == LatLon(  0.0,   0.0)
    assert travel(LatLon(0.0, 0), deg_to_km( 10), 0.0) == LatLon( 10.0,   0.0)
    assert travel(LatLon(0.0, 0), deg_to_km( 80), 0.0) == LatLon( 80.0,   0.0)
    assert travel(LatLon(0.0, 0), deg_to_km( 90), 0.0) == LatLon( 90.0,   0.0)
    assert travel(LatLon(0.0, 0), deg_to_km(100), 0.0) == LatLon( 80.0, 180.0)
    assert travel(LatLon(0.0, 0), deg_to_km(170), 0.0) == LatLon( 10.0, 180.0)
    assert travel(LatLon(0.0, 0), deg_to_km(180), 0.0) == LatLon(  0.0, 180.0)
    assert travel(LatLon(0.0, 0), deg_to_km(190), 0.0) == LatLon(-10.0, 180.0)
    assert travel(LatLon(0.0, 0), deg_to_km(260), 0.0) == LatLon(-80.0, 180.0)
    assert travel(LatLon(0.0, 0), deg_to_km(270), 0.0) == LatLon(-90.0, 180.0)
    assert travel(LatLon(0.0, 0), deg_to_km(280), 0.0) == LatLon(-80.0,   0.0)
    assert travel(LatLon(0.0, 0), deg_to_km(350), 0.0) == LatLon(-10.0,   0.0)
    assert travel(LatLon(0.0, 0), deg_to_km(360), 0.0) == LatLon(  0.0,   0.0)
    assert travel(LatLon(0.0, 0), deg_to_km(370), 0.0) == LatLon( 10.0,   0.0)

    assert travel(LatLon(10.0, 0), deg_to_km(  0), 0.0) == LatLon( 10.0,   0.0)
    assert travel(LatLon(10.0, 0), deg_to_km( 10), 0.0) == LatLon( 20.0,   0.0)
    assert travel(LatLon(10.0, 0), deg_to_km( 80), 0.0) == LatLon( 90.0,   0.0)
    assert travel(LatLon(10.0, 0), deg_to_km( 90), 0.0) == LatLon( 80.0, 180.0)
    assert travel(LatLon(10.0, 0), deg_to_km(100), 0.0) == LatLon( 70.0, 180.0)
    assert travel(LatLon(10.0, 0), deg_to_km(170), 0.0) == LatLon( 00.0, 180.0)
    assert travel(LatLon(10.0, 0), deg_to_km(180), 0.0) == LatLon(-10.0, 180.0)
    assert travel(LatLon(10.0, 0), deg_to_km(190), 0.0) == LatLon(-20.0, 180.0)
    assert travel(LatLon(10.0, 0), deg_to_km(260), 0.0) == LatLon(-90.0, 180.0)
    assert travel(LatLon(10.0, 0), deg_to_km(270), 0.0) == LatLon(-80.0,   0.0)
    assert travel(LatLon(10.0, 0), deg_to_km(280), 0.0) == LatLon(-70.0,   0.0)
    assert travel(LatLon(10.0, 0), deg_to_km(350), 0.0) == LatLon(  0.0,   0.0)
    assert travel(LatLon(10.0, 0), deg_to_km(360), 0.0) == LatLon( 10.0,   0.0)
    assert travel(LatLon(10.0, 0), deg_to_km(370), 0.0) == LatLon( 20.0,   0.0)

    assert travel(LatLon(80.0, 0), deg_to_km(  0), 0.0) == LatLon( 80.0,   0.0)
    assert travel(LatLon(80.0, 0), deg_to_km( 10), 0.0) == LatLon( 90.0,   0.0)
    assert travel(LatLon(80.0, 0), deg_to_km( 80), 0.0) == LatLon( 20.0, 180.0)
    assert travel(LatLon(80.0, 0), deg_to_km( 90), 0.0) == LatLon( 10.0, 180.0)
    assert travel(LatLon(80.0, 0), deg_to_km(100), 0.0) == LatLon(  0.0, 180.0)
    assert travel(LatLon(80.0, 0), deg_to_km(170), 0.0) == LatLon(-70.0, 180.0)
    assert travel(LatLon(80.0, 0), deg_to_km(180), 0.0) == LatLon(-80.0, 180.0)
    assert travel(LatLon(80.0, 0), deg_to_km(190), 0.0) == LatLon(-90.0, 180.0)
    assert travel(LatLon(80.0, 0), deg_to_km(260), 0.0) == LatLon(-20.0,   0.0)
    assert travel(LatLon(80.0, 0), deg_to_km(270), 0.0) == LatLon(-10.0,   0.0)
    assert travel(LatLon(80.0, 0), deg_to_km(280), 0.0) == LatLon(  0.0,   0.0)

    assert travel(LatLon(90.0, 0), deg_to_km(  0), 0.0) == LatLon( 90.0,   0.0)
    assert travel(LatLon(90.0, 0), deg_to_km(100), 0.0) == LatLon( 90.0,   0.0)

def test_travel_south():
    """Along circles of longitude"""
    assert travel(LatLon(90.0,   0.0), deg_to_km(  0), 180.0) == LatLon( 90.0,   0.0)
    assert travel(LatLon(90.0,   0.0), deg_to_km( 10), 180.0) == LatLon( 80.0,   0.0)
    assert travel(LatLon(90.0,   0.0), deg_to_km( 80), 180.0) == LatLon( 10.0,   0.0)
    assert travel(LatLon(90.0,   0.0), deg_to_km( 90), 180.0) == LatLon(  0.0,   0.0)
    assert travel(LatLon(90.0,   0.0), deg_to_km(100), 180.0) == LatLon(-10.0,   0.0)
    assert travel(LatLon(90.0,   0.0), deg_to_km(170), 180.0) == LatLon(-80.0,   0.0)
    assert travel(LatLon(90.0,   0.0), deg_to_km(180), 180.0) == LatLon(-90.0,   0.0)
    assert travel(LatLon(90.0,   0.0), deg_to_km(190), 180.0) == LatLon(-80.0, 180.0)
    assert travel(LatLon(90.0,   0.0), deg_to_km(260), 180.0) == LatLon(-10.0, 180.0)
    assert travel(LatLon(90.0,   0.0), deg_to_km(270), 180.0) == LatLon(  0.0, 180.0)
    assert travel(LatLon(90.0,   0.0), deg_to_km(280), 180.0) == LatLon( 10.0, 180.0)
    assert travel(LatLon(90.0,   0.0), deg_to_km(350), 180.0) == LatLon( 80.0, 180.0)
    assert travel(LatLon(90.0,   0.0), deg_to_km(360), 180.0) == LatLon( 90.0, 180.0)
    assert travel(LatLon(90.0,   0.0), deg_to_km(370), 180.0) == LatLon( 80.0,   0.0)

    assert travel(LatLon(80.0,   0.0), deg_to_km(  0), 180.0) == LatLon( 80.0,   0.0)
    assert travel(LatLon(80.0,   0.0), deg_to_km( 10), 180.0) == LatLon( 70.0,   0.0)
    assert travel(LatLon(80.0,   0.0), deg_to_km( 80), 180.0) == LatLon(  0.0,   0.0)
    assert travel(LatLon(80.0,   0.0), deg_to_km( 90), 180.0) == LatLon(-10.0,   0.0)
    assert travel(LatLon(80.0,   0.0), deg_to_km(100), 180.0) == LatLon(-20.0,   0.0)
    assert travel(LatLon(80.0,   0.0), deg_to_km(170), 180.0) == LatLon(-90.0,   0.0)
    assert travel(LatLon(80.0,   0.0), deg_to_km(180), 180.0) == LatLon(-80.0, 180.0)
    assert travel(LatLon(80.0,   0.0), deg_to_km(190), 180.0) == LatLon(-70.0, 180.0)
    assert travel(LatLon(80.0,   0.0), deg_to_km(260), 180.0) == LatLon(  0.0, 180.0)
    assert travel(LatLon(80.0,   0.0), deg_to_km(270), 180.0) == LatLon( 10.0, 180.0)
    assert travel(LatLon(80.0,   0.0), deg_to_km(280), 180.0) == LatLon( 20.0, 180.0)
    assert travel(LatLon(80.0,   0.0), deg_to_km(350), 180.0) == LatLon( 90.0, 180.0)
    assert travel(LatLon(80.0,   0.0), deg_to_km(360), 180.0) == LatLon( 80.0,   0.0)
    assert travel(LatLon(80.0,   0.0), deg_to_km(370), 180.0) == LatLon( 70.0,   0.0)

    assert travel(LatLon(10.0,   0.0), deg_to_km(  0), 180.0) == LatLon( 10.0,   0.0)
    assert travel(LatLon(10.0,   0.0), deg_to_km( 10), 180.0) == LatLon(  0.0,   0.0)
    assert travel(LatLon(10.0,   0.0), deg_to_km( 80), 180.0) == LatLon(-70.0,   0.0)
    assert travel(LatLon(10.0,   0.0), deg_to_km( 90), 180.0) == LatLon(-80.0,   0.0)
    assert travel(LatLon(10.0,   0.0), deg_to_km(100), 180.0) == LatLon(-90.0,   0.0)
    assert travel(LatLon(10.0,   0.0), deg_to_km(170), 180.0) == LatLon(-20.0, 180.0)
    assert travel(LatLon(10.0,   0.0), deg_to_km(180), 180.0) == LatLon(-10.0, 180.0)
    assert travel(LatLon(10.0,   0.0), deg_to_km(190), 180.0) == LatLon(  0.0, 180.0)
    assert travel(LatLon(10.0,   0.0), deg_to_km(260), 180.0) == LatLon( 70.0, 180.0)
    assert travel(LatLon(10.0,   0.0), deg_to_km(270), 180.0) == LatLon( 80.0, 180.0)
    assert travel(LatLon(10.0,   0.0), deg_to_km(280), 180.0) == LatLon( 90.0, 180.0)
    assert travel(LatLon(10.0,   0.0), deg_to_km(350), 180.0) == LatLon( 20.0,   0.0)
    assert travel(LatLon(10.0,   0.0), deg_to_km(360), 180.0) == LatLon( 10.0,   0.0)
    assert travel(LatLon(10.0,   0.0), deg_to_km(370), 180.0) == LatLon(  0.0,   0.0)

    assert travel(LatLon(0.0,   0.0), deg_to_km(  0), 180.0) == LatLon(  0.0,    0.0)
    assert travel(LatLon(0.0,   0.0), deg_to_km( 10), 180.0) == LatLon(-10.0,    0.0)
    assert travel(LatLon(0.0,   0.0), deg_to_km( 80), 180.0) == LatLon(-80.0,    0.0)
    assert travel(LatLon(0.0,   0.0), deg_to_km( 90), 180.0) == LatLon(-90.0,    0.0)
    assert travel(LatLon(0.0,  10.0), deg_to_km(100), 180.0) == LatLon(-80.0, -170.0)
    assert travel(LatLon(0.0,  80.0), deg_to_km(170), 180.0) == LatLon(-10.0, -100.0)
    assert travel(LatLon(0.0,  90.0), deg_to_km(180), 180.0) == LatLon(  0.0,  -90.0)
    assert travel(LatLon(0.0, 100.0), deg_to_km(190), 180.0) == LatLon( 10.0,  -80.0)
    assert travel(LatLon(0.0, 170.0), deg_to_km(260), 180.0) == LatLon( 80.0,  -10.0)
    assert travel(LatLon(0.0, 180.0), deg_to_km(270), 180.0) == LatLon( 90.0,    0.0)
    assert travel(LatLon(0.0,   0.0), deg_to_km(280), 180.0) == LatLon( 80.0,    0.0)
    assert travel(LatLon(0.0,   0.0), deg_to_km(350), 180.0) == LatLon( 10.0,    0.0)
    assert travel(LatLon(0.0,   0.0), deg_to_km(360), 180.0) == LatLon( 00.0,    0.0)
    assert travel(LatLon(0.0,   0.0), deg_to_km(370), 180.0) == LatLon(-10.0,    0.0)

    assert travel(LatLon(-10.0,    0.0), deg_to_km(  0), 180.0) == LatLon(-10.0,   0.0)
    assert travel(LatLon(-10.0,    0.0), deg_to_km( 10), 180.0) == LatLon(-20.0,   0.0)
    assert travel(LatLon(-10.0,    0.0), deg_to_km( 80), 180.0) == LatLon(-90.0,   0.0)
    assert travel(LatLon(-10.0, -180.0), deg_to_km( 90), 180.0) == LatLon(-80.0,   0.0)
    assert travel(LatLon(-10.0, -170.0), deg_to_km(100), 180.0) == LatLon(-70.0,  10.0)
    assert travel(LatLon(-10.0, -100.0), deg_to_km(170), 180.0) == LatLon(  0.0,  80.0)
    assert travel(LatLon(-10.0,  -90.0), deg_to_km(180), 180.0) == LatLon( 10.0,  90.0)
    assert travel(LatLon(-10.0,  -80.0), deg_to_km(190), 180.0) == LatLon( 20.0, 100.0)
    assert travel(LatLon(-10.0,    0.0), deg_to_km(260), 180.0) == LatLon( 90.0, 180.0)
    assert travel(LatLon(-10.0,    0.0), deg_to_km(270), 180.0) == LatLon( 80.0,   0.0)
    assert travel(LatLon(-10.0,    0.0), deg_to_km(280), 180.0) == LatLon( 70.0,   0.0)
    assert travel(LatLon(-10.0,    0.0), deg_to_km(350), 180.0) == LatLon(  0.0,   0.0)
    assert travel(LatLon(-10.0,    0.0), deg_to_km(360), 180.0) == LatLon(-10.0,   0.0)
    assert travel(LatLon(-10.0,    0.0), deg_to_km(370), 180.0) == LatLon(-20.0,   0.0)

    assert travel(LatLon(-80.0,   0.0), deg_to_km(  0), 180.0) == LatLon(-80.0,   0.0)
    assert travel(LatLon(-80.0,   0.0), deg_to_km( 10), 180.0) == LatLon(-90.0,   0.0)
    assert travel(LatLon(-80.0,   0.0), deg_to_km( 80), 180.0) == LatLon(-20.0, 180.0)
    assert travel(LatLon(-80.0,   0.0), deg_to_km( 90), 180.0) == LatLon(-10.0, 180.0)
    assert travel(LatLon(-80.0,   0.0), deg_to_km(100), 180.0) == LatLon(  0.0, 180.0)
    assert travel(LatLon(-80.0,   0.0), deg_to_km(170), 180.0) == LatLon( 70.0, 180.0)
    assert travel(LatLon(-80.0,   0.0), deg_to_km(180), 180.0) == LatLon( 80.0, 180.0)
    assert travel(LatLon(-80.0,   0.0), deg_to_km(190), 180.0) == LatLon( 90.0, 180.0)
    assert travel(LatLon(-80.0,   0.0), deg_to_km(260), 180.0) == LatLon( 20.0,   0.0)
    assert travel(LatLon(-80.0,   0.0), deg_to_km(270), 180.0) == LatLon( 10.0,   0.0)
    assert travel(LatLon(-80.0,   0.0), deg_to_km(280), 180.0) == LatLon(  0.0,   0.0)
    assert travel(LatLon(-80.0,   0.0), deg_to_km(350), 180.0) == LatLon(-70.0,   0.0)
    assert travel(LatLon(-80.0,   0.0), deg_to_km(360), 180.0) == LatLon(-80.0,   0.0)
    assert travel(LatLon(-80.0,   0.0), deg_to_km(369), 180.0) == LatLon(-89.0,   0.0)
    # Because of float imprecision, (360.0° + 10°) - 10° is not the same as 10°
    # That's why lon is still at 180° below...
    assert travel(LatLon(-80.0,   0.0), deg_to_km(370), 180.0) == LatLon(-90.0, 180.0)

    assert travel(LatLon(-90.0,   0.0), deg_to_km( 0), 180.0) == LatLon(-90.0,   0.0)
    assert travel(LatLon(-90.0,   0.0), deg_to_km(10), 180.0) == LatLon(-90.0,   0.0)

def test_travel_east():
    """Along circles of latitude"""
    assert travel(LatLon(90.0, 60.0), deg_to_km(100, 60.0), 90.0) == LatLon(90.0,   60.0)

     # Because of float imprecision, we get 180.00000000003, which leads to adjustment to -180.0
#    assert travel(LatLon(60.0, 0.0), deg_to_km(180, 60.0), 90.0) == LatLon(60.0, -180.0)

    assert travel(LatLon(60.0, 60.0), deg_to_km(  0, 60.0), 90.0) == LatLon(60.0,   60.0)
    assert travel(LatLon(60.0, 60.0), deg_to_km( 10, 60.0), 90.0) == LatLon(60.0,   70.0)
    assert travel(LatLon(60.0, 60.0), deg_to_km( 80, 60.0), 90.0) == LatLon(60.0,  140.0)
    assert travel(LatLon(60.0, 60.0), deg_to_km( 90, 60.0), 90.0) == LatLon(60.0,  150.0)
    assert travel(LatLon(60.0, 60.0), deg_to_km(100, 60.0), 90.0) == LatLon(60.0,  160.0)
    assert travel(LatLon(60.0, 60.0), deg_to_km(170, 60.0), 90.0) == LatLon(60.0, -130.0)
    assert travel(LatLon(60.0, 60.0), deg_to_km(180, 60.0), 90.0) == LatLon(60.0, -120.0)
    assert travel(LatLon(60.0, 60.0), deg_to_km(190, 60.0), 90.0) == LatLon(60.0, -110.0)
    assert travel(LatLon(60.0, 60.0), deg_to_km(260, 60.0), 90.0) == LatLon(60.0,  -40.0)
    assert travel(LatLon(60.0, 60.0), deg_to_km(270, 60.0), 90.0) == LatLon(60.0,  -30.0)
    assert travel(LatLon(60.0, 60.0), deg_to_km(280, 60.0), 90.0) == LatLon(60.0,  -20.0)
    assert travel(LatLon(60.0, 60.0), deg_to_km(350, 60.0), 90.0) == LatLon(60.0,   50.0)
    assert travel(LatLon(60.0, 60.0), deg_to_km(360, 60.0), 90.0) == LatLon(60.0,   60.0)
    assert travel(LatLon(60.0, 60.0), deg_to_km(370, 60.0), 90.0) == LatLon(60.0,   70.0)

    assert travel(LatLon(0.0, 0.0), deg_to_km(  0), 90.0) == LatLon(0,    0.0)
    assert travel(LatLon(0.0, 0.0), deg_to_km( 10), 90.0) == LatLon(0,   10.0)
    assert travel(LatLon(0.0, 0.0), deg_to_km( 80), 90.0) == LatLon(0,   80.0)
    assert travel(LatLon(0.0, 0.0), deg_to_km( 90), 90.0) == LatLon(0,   90.0)
    assert travel(LatLon(0.0, 0.0), deg_to_km(100), 90.0) == LatLon(0,  100.0)
    assert travel(LatLon(0.0, 0.0), deg_to_km(170), 90.0) == LatLon(0,  170.0)
    assert travel(LatLon(0.0, 0.0), deg_to_km(180), 90.0) == LatLon(0,  180.0)
    assert travel(LatLon(0.0, 0.0), deg_to_km(190), 90.0) == LatLon(0, -170.0)
    assert travel(LatLon(0.0, 0.0), deg_to_km(260), 90.0) == LatLon(0, -100.0)
    assert travel(LatLon(0.0, 0.0), deg_to_km(270), 90.0) == LatLon(0,  -90.0)
    assert travel(LatLon(0.0, 0.0), deg_to_km(280), 90.0) == LatLon(0,  -80.0)
    assert travel(LatLon(0.0, 0.0), deg_to_km(350), 90.0) == LatLon(0,  -10.0)
    assert travel(LatLon(0.0, 0.0), deg_to_km(360), 90.0) == LatLon(0,    0.0)
    assert travel(LatLon(0.0, 0.0), deg_to_km(370), 90.0) == LatLon(0,   10.0)

    assert travel(LatLon(-45.0, -170.0), deg_to_km(  0, -45.0), 90.0) == LatLon(-45.0, -170.0)
    assert travel(LatLon(-45.0, -170.0), deg_to_km( 10, -45.0), 90.0) == LatLon(-45.0, -160.0)
    assert travel(LatLon(-45.0, -170.0), deg_to_km( 80, -45.0), 90.0) == LatLon(-45.0,  -90.0)
    assert travel(LatLon(-45.0, -170.0), deg_to_km( 90, -45.0), 90.0) == LatLon(-45.0,  -80.0)
    assert travel(LatLon(-45.0, -170.0), deg_to_km(100, -45.0), 90.0) == LatLon(-45.0,  -70.0)
    assert travel(LatLon(-45.0, -170.0), deg_to_km(170, -45.0), 90.0) == LatLon(-45.0,    0.0)
    assert travel(LatLon(-45.0, -170.0), deg_to_km(180, -45.0), 90.0) == LatLon(-45.0,   10.0)
    assert travel(LatLon(-45.0, -170.0), deg_to_km(190, -45.0), 90.0) == LatLon(-45.0,   20.0)
    assert travel(LatLon(-45.0, -170.0), deg_to_km(260, -45.0), 90.0) == LatLon(-45.0,   90.0)
    assert travel(LatLon(-45.0, -170.0), deg_to_km(270, -45.0), 90.0) == LatLon(-45.0,  100.0)
    assert travel(LatLon(-45.0, -170.0), deg_to_km(280, -45.0), 90.0) == LatLon(-45.0,  110.0)
    assert travel(LatLon(-45.0, -170.0), deg_to_km(350, -45.0), 90.0) == LatLon(-45.0,  180.0)
    assert travel(LatLon(-45.0, -170.0), deg_to_km(360, -45.0), 90.0) == LatLon(-45.0, -170.0)
    assert travel(LatLon(-45.0, -170.0), deg_to_km(370, -45.0), 90.0) == LatLon(-45.0, -160.0)

def test_travel_west():
    """Along circles of latitude"""
    assert travel(LatLon(90.0, -180.0), deg_to_km(100, 90.0), 270.0) == LatLon(90.0, -180.0)

    assert travel(LatLon(80.0, -180.0), deg_to_km(  0, 80.0), 270.0) == LatLon(80.0, -180.0)
    assert travel(LatLon(80.0, -180.0), deg_to_km( 10, 80.0), 270.0) == LatLon(80.0,  170.0)
    assert travel(LatLon(80.0, -180.0), deg_to_km( 80, 80.0), 270.0) == LatLon(80.0,  100.0)
    assert travel(LatLon(80.0, -180.0), deg_to_km( 90, 80.0), 270.0) == LatLon(80.0,   90.0)
    assert travel(LatLon(80.0, -180.0), deg_to_km(100, 80.0), 270.0) == LatLon(80.0,   80.0)
    assert travel(LatLon(80.0, -180.0), deg_to_km(170, 80.0), 270.0) == LatLon(80.0,   10.0)
    assert travel(LatLon(80.0, -180.0), deg_to_km(180, 80.0), 270.0) == LatLon(80.0,    0.0)
    assert travel(LatLon(80.0, -180.0), deg_to_km(190, 80.0), 270.0) == LatLon(80.0,  -10.0)
    assert travel(LatLon(80.0, -180.0), deg_to_km(260, 80.0), 270.0) == LatLon(80.0,  -80.0)
    assert travel(LatLon(80.0, -180.0), deg_to_km(270, 80.0), 270.0) == LatLon(80.0,  -90.0)
    assert travel(LatLon(80.0, -180.0), deg_to_km(280, 80.0), 270.0) == LatLon(80.0, -100.0)
    assert travel(LatLon(80.0, -180.0), deg_to_km(350, 80.0), 270.0) == LatLon(80.0, -170.0)
    assert travel(LatLon(80.0, -180.0), deg_to_km(360, 80.0), 270.0) == LatLon(80.0,  180.0)
    assert travel(LatLon(80.0, -180.0), deg_to_km(370, 80.0), 270.0) == LatLon(80.0,  170.0)

    assert travel(LatLon(0.0, -10.0), deg_to_km(  0), 270.0) == LatLon(0.0,  -10.0)
    assert travel(LatLon(0.0, -10.0), deg_to_km( 10), 270.0) == LatLon(0.0,  -20.0)
    assert travel(LatLon(0.0, -10.0), deg_to_km( 80), 270.0) == LatLon(0.0,  -90.0)
    assert travel(LatLon(0.0, -10.0), deg_to_km( 90), 270.0) == LatLon(0.0, -100.0)
    assert travel(LatLon(0.0, -10.0), deg_to_km(100), 270.0) == LatLon(0.0, -110.0)
    assert travel(LatLon(0.0, -10.0), deg_to_km(170), 270.0) == LatLon(0.0, -180.0)
    assert travel(LatLon(0.0, -10.0), deg_to_km(180), 270.0) == LatLon(0.0,  170.0)
    assert travel(LatLon(0.0, -10.0), deg_to_km(190), 270.0) == LatLon(0.0,  160.0)
    assert travel(LatLon(0.0, -10.0), deg_to_km(260), 270.0) == LatLon(0.0,   90.0)
    assert travel(LatLon(0.0, -10.0), deg_to_km(270), 270.0) == LatLon(0.0,   80.0)
    assert travel(LatLon(0.0, -10.0), deg_to_km(280), 270.0) == LatLon(0.0,   70.0)
    assert travel(LatLon(0.0, -10.0), deg_to_km(350), 270.0) == LatLon(0.0,    0.0)
    assert travel(LatLon(0.0, -10.0), deg_to_km(360), 270.0) == LatLon(0.0,  -10.0)
    assert travel(LatLon(0.0, -10.0), deg_to_km(370), 270.0) == LatLon(0.0,  -20.0)

    assert travel(LatLon(-30.0, 180.0), deg_to_km(  0, -30.0), 270.0) == LatLon(-30.0,  180.0)
    assert travel(LatLon(-30.0, 180.0), deg_to_km( 10, -30.0), 270.0) == LatLon(-30.0,  170.0)
    assert travel(LatLon(-30.0, 180.0), deg_to_km( 80, -30.0), 270.0) == LatLon(-30.0,  100.0)
    assert travel(LatLon(-30.0, 180.0), deg_to_km( 90, -30.0), 270.0) == LatLon(-30.0,   90.0)
    assert travel(LatLon(-30.0, 180.0), deg_to_km(100, -30.0), 270.0) == LatLon(-30.0,   80.0)
    assert travel(LatLon(-30.0, 180.0), deg_to_km(170, -30.0), 270.0) == LatLon(-30.0,   10.0)
    assert travel(LatLon(-30.0, 180.0), deg_to_km(180, -30.0), 270.0) == LatLon(-30.0,    0.0)
    assert travel(LatLon(-30.0, 180.0), deg_to_km(190, -30.0), 270.0) == LatLon(-30.0,  -10.0)
    assert travel(LatLon(-30.0, 180.0), deg_to_km(260, -30.0), 270.0) == LatLon(-30.0,  -80.0)
    assert travel(LatLon(-30.0, 180.0), deg_to_km(270, -30.0), 270.0) == LatLon(-30.0,  -90.0)
    assert travel(LatLon(-30.0, 180.0), deg_to_km(280, -30.0), 270.0) == LatLon(-30.0, -100.0)
    assert travel(LatLon(-30.0, 180.0), deg_to_km(350, -30.0), 270.0) == LatLon(-30.0, -170.0)
    assert travel(LatLon(-30.0, 180.0), deg_to_km(360, -30.0), 270.0) == LatLon(-30.0,  180.0)
    assert travel(LatLon(-30.0, 180.0), deg_to_km(370, -30.0), 270.0) == LatLon(-30.0,  170.0)

### Cross equator and/or 0-meridian like in 1.pdn

def test_travel_1_q1_q2():
    """Q1 -> Q2"""
    assert(isclose(calc_bearing(LatLon(30.0, 30.0), LatLon(-30.0, 15.0)), 194.7514449152269))
    assert(isclose(calc_distance(LatLon(30.0, 30.0), LatLon(-30.0, 15.0)), 6858.150413856773))
    assert(travel(LatLon(30.0, 30.0), 6858.150413856773, 194.7514449152269) == LatLon(-30.0, 15.0))

def test_travel_1_q1_q3():
    """Q1 -> Q3"""
    assert(isclose(calc_bearing(LatLon(30.0, 30.0), LatLon(-30.0, -15.0)), 219.63927223775613))
    assert(isclose(calc_distance(LatLon(30.0, 30.0), LatLon(-30.0, -15.0)), 8197.30142711796))
    assert(travel(LatLon(30.0, 30.0), 8197.30142711796, 219.63927223775613) == LatLon(-30.0, -15.0))

def test_travel_1_q1_q4():
    """Q1 -> Q4"""
    assert(isclose(calc_bearing(LatLon(30.0, 30.0), LatLon(-15.0, -15.0)), 230.36948571096076))
    assert(isclose(calc_distance(LatLon(30.0, 30.0), LatLon(-15.0, -15.0)), 6947.182442673351))
    assert(travel(LatLon(30.0, 30.0), 6947.182442673351, 230.36948571096076) == LatLon(-15.0, -15.0))

def test_travel_1_q2_q1():
    """Q2 -> Q1"""
    assert(isclose(calc_bearing(LatLon(-30.0, 30.0), LatLon(30.0, 15.0)), 345.2485550847731))
    assert(isclose(calc_distance(LatLon(-30.0, 30.0), LatLon(30.0, 15.0)), 6858.150413856773))
    assert(travel(LatLon(-30.0, 30.0), 6858.150413856773, 345.2485550847731) == LatLon(30.0, 15.0))

def test_travel_1_q2_q3():
    """Q2 -> Q3"""
    assert(isclose(calc_bearing(LatLon(-30.0, 30.0), LatLon(-15.0, -15.0)), 279.74995402797686))
    assert(isclose(calc_distance(LatLon(-30.0, 30.0), LatLon(-15.0, -15.0)), 4878.105519870221))
    assert(travel(LatLon(-30.0, 30.0), 4878.105519870221, 279.74995402797686) == LatLon(-15.0, -15.0))

def test_travel_1_q2_q4():
    """Q2 -> Q4"""
    assert(isclose(calc_bearing(LatLon(-30.0, 30.0), LatLon(30.0, -15.0)), 320.36072776224387))
    assert(isclose(calc_distance(LatLon(-30.0, 30.0), LatLon(30.0, -15.0)), 8197.30142711796))
    assert(travel(LatLon(-30.0, 30.0), 8197.30142711796, 320.36072776224387) == LatLon(30.0, -15.0))

def test_travel_1_q3_q1():
    """Q3 -> Q1"""
    assert(isclose(calc_bearing(LatLon(-30.0, -30.0), LatLon(30.0, 15.0)), 39.63927223775613))
    assert(isclose(calc_distance(LatLon(-30.0, -30.0), LatLon(30.0, 15.0)), 8197.30142711796))
    assert(travel(LatLon(-30.0, -30.0), 8197.30142711796, 39.63927223775613) == LatLon(30.0, 15.0))

def test_travel_1_q3_q2():
    """Q3 -> Q2"""
    assert(isclose(calc_bearing(LatLon(-30.0, -30.0), LatLon(-15.0, -15.0)), 45.88869972297674))
    assert(isclose(calc_distance(LatLon(-30.0, -30.0), LatLon(-15.0, -15.0)), 2265.8122607469577))
    assert(travel(LatLon(-30.0, -30.0), 2265.8122607469577, 45.88869972297674) == LatLon(-15.0, -15.0))

def test_travel_1_q3_q4():
    """Q3 -> Q4"""
    assert(isclose(calc_bearing(LatLon(-30.0, -30.0), LatLon(30.0, -15.0)), 14.751444915226907))
    assert(isclose(calc_distance(LatLon(-30.0, -30.0), LatLon(30.0, -15.0)), 6858.150413856773))
    assert(travel(LatLon(-30.0, -30.0), 6858.150413856773, 14.751444915226907) == LatLon(30.0, -15.0))

def test_travel_1_q4_q1():
    """Q4 -> Q1"""
    assert(isclose(calc_bearing(LatLon(30.0, -30.0), LatLon(15.0, 15.0)), 99.74995402797683))
    assert(isclose(calc_distance(LatLon(30.0, -30.0), LatLon(15.0, 15.0)), 4878.105519870221))
    assert(travel(LatLon(30.0, -30.0), 4878.105519870221, 99.74995402797683) == LatLon(15.0, 15.0))

def test_travel_1_q4_q2():
    """Q4 -> Q2"""
    assert(isclose(calc_bearing(LatLon(30.0, -30.0), LatLon(-30.0, 15.0)), 140.36072776224387))
    assert(isclose(calc_distance(LatLon(30.0, -30.0), LatLon(-30.0, 15.0)), 8197.30142711796))
    assert(travel(LatLon(30.0, -30.0), 8197.30142711796, 140.36072776224387) == LatLon(-30.0, 15.0))

def test_travel_1_q4_q3():
    """Q4 -> Q3"""
    assert(isclose(calc_bearing(LatLon(30.0, -30.0), LatLon(-30.0, -15.0)), 165.2485550847731))
    assert(isclose(calc_distance(LatLon(30.0, -30.0), LatLon(-30.0, -15.0)), 6858.150413856773))
    assert(travel(LatLon(30.0, -30.0), 6858.150413856773, 165.2485550847731) == LatLon(-30.0, -15.0))

### Cross equator and/or 0-meridian like in 2.pdn

def test_travel_2_q1_q2():
    """Q1 -> Q2"""
    assert(isclose(calc_bearing(LatLon(30.0, -150.0), LatLon(-30.0, -165.0)), 194.7514449152269))
    assert(isclose(calc_distance(LatLon(30.0, -150.0), LatLon(-30.0, -165.0)), 6858.150413856773))
    assert(travel(LatLon(30.0, -150.0), 6858.150413856773, 194.7514449152269) == LatLon(-30.0, -165.0))

def test_travel_2_q1_q3():
    """Q1 -> Q3"""
    assert(isclose(calc_bearing(LatLon(30.0, -150.0), LatLon(-30.0, 165.0)), 219.63927223775613))
    assert(isclose(calc_distance(LatLon(30.0, -150.0), LatLon(-30.0, 165.0)), 8197.30142711796))
    assert(travel(LatLon(30.0, -150.0), 8197.30142711796, 219.63927223775613) == LatLon(-30.0, 165.0))

def test_travel_2_q1_q4():
    """Q1 -> Q4"""
    assert(isclose(calc_bearing(LatLon(30.0, -150.0), LatLon(15.0, 165)), 260.25004597202314))
    assert(isclose(calc_distance(LatLon(30.0, -150.0), LatLon(15.0, 165)), 4878.1055198702215))
    assert(travel(LatLon(30.0, -150.0), 4878.1055198702215, 260.25004597202314) == LatLon(15.0, 165))

def test_travel_2_q2_q1():
    """Q2 -> Q1"""
    assert(isclose(calc_bearing(LatLon(-30.0, -150.0), LatLon(30.0, -165.0)), 345.2485550847731))
    assert(isclose(calc_distance(LatLon(-30.0, -150.0), LatLon(30.0, -165.0)), 6858.150413856773))
    assert(travel(LatLon(-30.0, -150.0), 6858.150413856773, 345.2485550847731) == LatLon(30.0, -165.0))

def test_travel_2_q2_q3():
    """Q2 -> Q3"""
    assert(isclose(calc_bearing(LatLon(-30.0, -150.0), LatLon(-15.0, 165.0)), 279.7499540279768))
    assert(isclose(calc_distance(LatLon(-30.0, -150.0), LatLon(-15.0, 165.0)), 4878.1055198702215))
    assert(travel(LatLon(-30.0, -150.0), 4878.1055198702215, 279.7499540279768) == LatLon(-15.0, 165.0))

def test_travel_2_q2_q4():
    """Q2 -> Q4"""
    assert(isclose(calc_bearing(LatLon(-30.0, -150.0), LatLon(15.0, 165.0)), 309.63051428903924))
    assert(isclose(calc_distance(LatLon(-30.0, -150.0), LatLon(15.0, 165.0)), 6947.182442673351))
    assert(travel(LatLon(-30.0, -150.0), 6947.182442673351, 309.63051428903924) == LatLon(15.0, 165.0))

def test_travel_2_q3_q1():
    """Q3 -> Q1"""
    assert(isclose(calc_bearing(LatLon(-30.0, 150.0), LatLon(30.0, -165.0)), 39.639272237756146))
    assert(isclose(calc_distance(LatLon(-30.0, 150.0), LatLon(30.0, -165.0)), 8197.30142711796))
    assert(travel(LatLon(-30.0, 150.0), 8197.30142711796, 39.639272237756146) == LatLon(30.0, -165.0))

def test_travel_2_q3_q2():
    """Q3 -> Q2"""
    assert(isclose(calc_bearing(LatLon(-30.0, 150.0), LatLon(-15.0, -165.0)), 80.25004597202319))
    assert(isclose(calc_distance(LatLon(-30.0, 150.0), LatLon(-15.0, -165.0)), 4878.1055198702215))
    assert(travel(LatLon(-30.0, 150.0), 4878.1055198702215, 80.25004597202319) == LatLon(-15.0, -165.0))

def test_travel_2_q3_q4():
    """Q3 -> Q4"""
    assert(isclose(calc_bearing(LatLon(-30.0, 150.0), LatLon(30.0, 165.0)), 14.751444915226907))
    assert(isclose(calc_distance(LatLon(-30.0, 150.0), LatLon(30.0, 165.0)), 6858.150413856773))
    assert(travel(LatLon(-30.0, 150.0), 6858.150413856773, 14.751444915226907) == LatLon(30.0, 165.0))

def test_travel_2_q4_q1():
    """Q4 -> Q1"""
    assert(isclose(calc_bearing(LatLon(30.0, 150.0), LatLon(15.0, 165.0)), 134.11130027702328))
    assert(isclose(calc_distance(LatLon(30.0, 150.0), LatLon(15.0, 165.0)), 2265.8122607469577))
    assert(travel(LatLon(30.0, 150.0), 2265.8122607469577, 134.11130027702328) == LatLon(15.0, 165.0))

def test_travel_2_q4_q2():
    """Q4 -> Q2"""
    assert(isclose(calc_bearing(LatLon(30.0, 150.0), LatLon(-30.0, -165.0)), 140.36072776224387))
    assert(isclose(calc_distance(LatLon(30.0, 150.0), LatLon(-30.0, -165.0)), 8197.30142711796))
    assert(travel(LatLon(30.0, 150.0), 8197.30142711796, 140.36072776224387) == LatLon(-30.0, -165.0))

def test_travel_2_q4_q3():
    """Q4 -> Q3"""
    assert(isclose(calc_bearing(LatLon(30.0, 150.0), LatLon(-30.0, 165.0)), 165.2485550847731))
    assert(isclose(calc_distance(LatLon(30.0, 150.0), LatLon(-30.0, 165.0)), 6858.150413856773))
    assert(travel(LatLon(30.0, 150.0), 6858.150413856773, 165.2485550847731) == LatLon(-30.0, 165.0))

### Travel to a point of same latitude, as in 3.pdn

def test_travel_3_a_b():
    """A -> B"""
    assert(isclose(calc_bearing(LatLon(60.0, 15.0), LatLon(60.0, -150.0)), 351.35612163513326))
    assert(isclose(calc_distance(LatLon(60.0, 15.0), LatLon(60.0, -150.0)), 6608.848934146663))
    assert(travel(LatLon(60.0, 15.0), 6608.848934146663, 351.35612163513326) == LatLon(60.0, -150.0))

def test_travel_3_a_c():
    """A-> C"""
    assert(isclose(calc_bearing(LatLon(60.0, 15.0), LatLon(60.0, 150.0)), 25.56144583679776))
    assert(isclose(calc_distance(LatLon(60.0, 15.0), LatLon(60.0, 150.0)), 6118.467805800631))
    assert(travel(LatLon(60.0, 15.0), 6118.467805800631, 25.56144583679776) == LatLon(60.0, 150.0))

def test_travel_3_b_c():
    """B -> C"""
    assert(isclose(calc_bearing(LatLon(60.0, -150.0), LatLon(60.0, 150.0)), 296.56505117707798))
    assert(isclose(calc_distance(LatLon(60.0, -150.0), LatLon(60.0, 150.0)), 3219.6522077283666))
    assert(travel(LatLon(60.0, -150.0), 3219.6522077283666, 296.56505117707798) == LatLon(60.0, 150.0))

def test_travel_3_c_b():
    """C -> B"""
    assert(isclose(calc_bearing(LatLon(60.0, 150.0), LatLon(60.0, -150.0)), 63.43494882292202))
    assert(isclose(calc_distance(LatLon(60.0, 150.0), LatLon(60.0, -150.0)), 3219.6522077283666))
    assert(travel(LatLon(60.0, 150.0), 3219.6522077283666, 63.43494882292202) == LatLon(60.0, -150.0))

def test_travel_3_d_c():
    """D -> B"""
    assert(isclose(calc_bearing(LatLon(60.0, -90.0), LatLon(60.0, 150.0)), 326.30993247402023))
    assert(isclose(calc_distance(LatLon(60.0, -90.0), LatLon(60.0, 150.0)), 5706.281104765323))
    assert(travel(LatLon(60.0, -90.0), 5706.281104765323, 326.30993247402023) == LatLon(60.0, 150.0))

def test_travel_3_d_e():
    """D -> C"""
    assert(isclose(calc_bearing(LatLon(60.0, -90.0), LatLon(60.0, 60.0)), 17.192123734020974))
    assert(isclose(calc_distance(LatLon(60.0, -90.0), LatLon(60.0, 60.0)), 6422.418272993739))
    assert(travel(LatLon(60.0, -90.0), 6422.418272993739, 17.192123734020974) == LatLon(60.0, 60.0))

### Travel to a point of same latitude, as in 4.pdn

def test_travel_4_a_b():
    """A -> B"""
    assert(isclose(calc_bearing(LatLon(-60.0, 100.0), LatLon(-60.0, -150.0)), 141.04342059936801))
    assert(isclose(calc_distance(LatLon(-60.0, 100.0), LatLon(-60.0, -150.0)), 5376.987893935466))
    assert(travel(LatLon(-60.0, 100.0), 5376.987893935466, 141.04342059936801) == LatLon(-60.0, -150.0))

def test_travel_4_a_c():
    """A -> C"""
    assert(isclose(calc_bearing(LatLon(-60.0, 100.0), LatLon(-60.0, -30.0)), 208.30005243274795))
    assert(isclose(calc_distance(LatLon(-60.0, 100.0), LatLon(-60.0, -30.0)), 5992.565597324029))
    assert(travel(LatLon(-60.0, 100.0), 5992.565597324029, 208.30005243274795) == LatLon(-60.0, -30.0))

def test_travel_4_b_c():
    """B -> C"""
    assert(isclose(calc_bearing(LatLon(-60.0, -150.0), LatLon(-60.0, -30.0)), 146.30993247402023))
    assert(isclose(calc_distance(LatLon(-60.0, -150.0), LatLon(-60.0, -30.0)), 5706.281104765322))
    assert(travel(LatLon(-60.0, -150.0), 5706.281104765322, 146.30993247402023) == LatLon(-60.0, -30.0))

def test_travel_4_c_b():
    """C -> B"""
    assert(isclose(calc_bearing(LatLon(-60.0, -30.0), LatLon(-60.0, -150.0)), 213.69006752597977))
    assert(isclose(calc_distance(LatLon(-60.0, -30.0), LatLon(-60.0, -150.0)), 5706.281104765322))
    assert(travel(LatLon(-60.0, -30.0), 5706.281104765322, 213.69006752597977) == LatLon(-60.0, -150.0))
