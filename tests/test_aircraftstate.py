"""Test whether incomplete AicraftState raises InsufficientData"""

import pytest
from notify import AicraftState, InsufficientData


def test_state_111111():
    """All required data present"""
    assert AicraftState(
        ["3de53c", "CHX24   ", "D-HHBG", "0020", 52.199765, 7.772232, 1100, 0, 0, None]
    )


def test_state_011111():
    """ICAO hex missing, which is OK"""
    assert AicraftState(
        [None, "CHX24   ", "D-HHBG", "0020", 52.199765, 7.772232, 1100, 0, 0, None]
    )


def test_state_101111():
    """Callsign missing, which is OK"""
    assert AicraftState(
        ["3de53c", None, "D-HHBG", "0020", 52.199765, 7.772232, 1100, 0, 0, None]
    )


def test_state_001111():
    """ICAO hex and callsign missing, which is OK"""
    assert AicraftState(
        [None, None, "D-HHBG", "0020", 52.199765, 7.772232, 1100, 0, 0, None]
    )


def test_state_110111():
    """Reg missing, which is OK"""
    assert AicraftState(
        ["3de53c", "CHX24   ", None, "0020", 52.199765, 7.772232, 1100, 0, 0, None]
    )


def test_state_010111():
    """ICAO hex and reg missing, which is OK"""
    assert AicraftState(
        [None, "CHX24   ", None, "0020", 52.199765, 7.772232, 1100, 0, 0, None]
    )


def test_state_100111():
    """Callsign and reg  missing, which is OK"""
    assert AicraftState(
        ["3de53c", None, None, "0020", 52.199765, 7.772232, 1100, 0, 0, None]
    )


def test_state_000111():
    """ICAO hex, callsign and reg missing, at least one is required"""
    with pytest.raises(InsufficientData):
        AicraftState([None, None, None, "0020", 52.199765, 7.772232, 1100, 0, 0, None])


def test_state_111011():
    """lat missing, which is required"""
    with pytest.raises(InsufficientData):
        assert AicraftState(
            ["3de53c", "CHX24   ", "D-HHBG", "0020", None, 7.772232, 1100, 0, 0, None]
        )


def test_state_111101():
    """lon missing, which is required"""
    with pytest.raises(InsufficientData):
        assert AicraftState(
            ["3de53c", "CHX24   ", "D-HHBG", "0020", 52.199765, None, 1100, 0, 0, None]
        )


def test_state_111001():
    """lat,lon missing, which is required"""
    with pytest.raises(InsufficientData):
        assert AicraftState(
            ["3de53c", "CHX24   ", "D-HHBG", "0020", None, None, 1100, 0, 0, None]
        )


def test_state_111110():
    """track missing, which is required"""
    with pytest.raises(InsufficientData):
        assert AicraftState(
            [
                "3de53c",
                "CHX24   ",
                "D-HHBG",
                "0020",
                52.199765,
                7.772232,
                1100,
                0,
                None,
                None,
            ]
        )


def test_state_111010():
    """lat and track missing, which is required"""
    with pytest.raises(InsufficientData):
        assert AicraftState(
            [
                "3de53c",
                "CHX24   ",
                "D-HHBG",
                "0020",
                None,
                7.772232,
                1100,
                0,
                None,
                None,
            ]
        )


def test_state_111100():
    """lon missing, which is required"""
    with pytest.raises(InsufficientData):
        assert AicraftState(
            [
                "3de53c",
                "CHX24   ",
                "D-HHBG",
                "0020",
                52.199765,
                None,
                1100,
                0,
                None,
                None,
            ]
        )


def test_state_111000():
    """latlong and track missing, which is required"""
    with pytest.raises(InsufficientData):
        assert AicraftState(
            ["3de53c", "CHX24   ", "D-HHBG", "0020", None, None, 1100, 0, None, None]
        )
