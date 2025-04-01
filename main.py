import sys
from PyQt5 import QtWidgets
from components.gui import MainWindow
from components.load import load_config, load_teams


def main():
    app = QtWidgets.QApplication(sys.argv)
    dropdown_config = load_config("config/dropdown_config.json")
    teams_list, teams_dict = load_teams("config/teams.json")
    window = MainWindow(dropdown_config, teams_list)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
