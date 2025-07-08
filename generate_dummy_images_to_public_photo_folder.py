import os
from pathlib import Path
import xml.etree.ElementTree as ET
from components.load import load_config
import cairosvg
from components.svg_generator import generate_match_list_svg
from components.match import Match

DUMMY_FILENAME = "C:/Users/Public/Pictures/matchday-announcement-debug.png"

DUMMY_DATA = [
    {
        "home": "home",
        "home_suffix": "home_suffix",
        "away": "away",
        "away_suffix": "away_suffix",
        "day": "day",
        "time": "time",
        "league": "league",
        "age_class": "age_class",
        "sport": "Fußball",
        "home_score": "home_score",
        "away_score": "away_score",
        "other": "other"
    },
    {
        "home": "Team A",
        "home_suffix": "",
        "away": "Team B",
        "away_suffix": "II",
        "day": "Montag",
        "time": "18:30",
        "league": "Bezirksliga",
        "age_class": "D-Junioren",
        "sport": "Fußball",
        "home_score": "3",
        "away_score": "2",
        "other": "verschoben"
    },
    {
        "home": "Team A",
        "home_suffix": "",
        "away": "Team B",
        "away_suffix": "II",
        "day": "16.05.",
        "time": "18:30",
        "league": "Bezirksliga",
        "age_class": "D-Junioren",
        "sport": "Fußball",
        "home_score": "",
        "away_score": "",
        "other": ""
    },
    {
        "home": "EXTREMLANGERTEAMNAME",
        "home_suffix": "",
        "away": "FC Förderkader Renè Schneider",
        "away_suffix": "II",
        "day": "16.05.",
        "time": "18:30",
        "league": "EXTREMLANGELIGA",
        "age_class": "EXTREMLANGEALTERSKLASSE",
        "sport": "Fußball",
        "home_score": "",
        "away_score": "",
        "other": "EXTREMLANGERGRUND"
    },
    {
        "home": "Team A",
        "home_suffix": "",
        "away": "Team B",
        "away_suffix": "II",
        "day": "Montag",
        "time": "18:30",
        "league": "Verbandsliga",
        "age_class": "Frauen",
        "sport": "Volleyball",
        "home_score": "3",
        "away_score": "2",
        "other": "verschoben"
    },
    {
        "home": "Team A",
        "home_suffix": "",
        "away": "Team B",
        "away_suffix": "II",
        "day": "Montag",
        "time": "18:30",
        "league": "Landesliga",
        "age_class": "U19",
        "sport": "Tischtennis",
        "home_score": "3",
        "away_score": "2",
        "other": "verschoben"
    }
]
DUMMY_MATCHES = [Match.from_dict(item) for item in DUMMY_DATA]

if __name__ == "__main__":
    generate_match_list_svg(DUMMY_MATCHES, DUMMY_FILENAME, True)
