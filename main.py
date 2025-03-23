import sys
from PyQt5 import QtWidgets
from components.config import load_config
from components.gui import MainWindow
import json


def main():
    app = QtWidgets.QApplication(sys.argv)
    config = load_config()
    teams_list, teams_dict = load_teams()
    window = MainWindow(config, teams_list)
    window.show()
    sys.exit(app.exec_())


def load_teams(filename="teams.json"):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    teams = data.get("teams", [])
    team_dict = {team["name"]: team["logo"] for team in teams}
    team_names = list(team_dict.keys())
    return team_names, team_dict


if __name__ == "__main__":
    main()
