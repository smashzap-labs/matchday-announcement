from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
import os
import json
from components.match import Match
from components.svg_generator import generate_match_list_svg


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, config, teams_list):
        super().__init__()
        self.config = config
        self.teams_list = teams_list  # Liste möglicher Vereinsnamen für Auto-Vervollständigung
        self.matches = []  # Hier werden die gespeicherten Spiele abgelegt
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Spieltag-Manager")
        central = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout()

        # Formular-Layout
        form_layout = QtWidgets.QFormLayout()

        # Heimverein: QLineEdit mit Auto-Vervollständigung und Suffix-Eingabe
        self.home_team_edit = QtWidgets.QLineEdit()
        completer_home = QtWidgets.QCompleter(self.teams_list)
        completer_home.setCaseSensitivity(Qt.CaseInsensitive)
        self.home_team_edit.setCompleter(completer_home)
        self.home_suffix_edit = QtWidgets.QLineEdit()
        self.home_suffix_edit.setFixedWidth(30)
        home_layout = QtWidgets.QHBoxLayout()
        home_layout.addWidget(self.home_team_edit)
        home_layout.addWidget(self.home_suffix_edit)
        form_layout.addRow("Heim:", home_layout)

        # Gastverein: QLineEdit mit Auto-Vervollständigung und Suffix-Eingabe
        self.away_team_edit = QtWidgets.QLineEdit()
        completer_away = QtWidgets.QCompleter(self.teams_list)
        completer_away.setCaseSensitivity(Qt.CaseInsensitive)
        self.away_team_edit.setCompleter(completer_away)
        self.away_suffix_edit = QtWidgets.QLineEdit()
        self.away_suffix_edit.setFixedWidth(30)
        away_layout = QtWidgets.QHBoxLayout()
        away_layout.addWidget(self.away_team_edit)
        away_layout.addWidget(self.away_suffix_edit)
        form_layout.addRow("Gast:", away_layout)

        # Sport-Feld
        self.sport_combo = QtWidgets.QComboBox()
        self.sport_combo.addItems(self.config.get("sports", []))
        form_layout.addRow("Sport:", self.sport_combo)

        # Radio-Buttons für den Spieltag (Tage aus config.json)
        self.day_group = QtWidgets.QButtonGroup(self)
        day_layout = QtWidgets.QHBoxLayout()
        self.day_buttons = []
        for day in self.config.get("days", []):
            rb = QtWidgets.QRadioButton(day)
            self.day_group.addButton(rb)
            day_layout.addWidget(rb)
            self.day_buttons.append(rb)
        form_layout.addRow("Tag:", day_layout)

        # Dropdown für die Uhrzeit (aus config.json)
        self.time_combo = QtWidgets.QComboBox()
        times = self.config.get("times", [])
        if not times:
            times = [f"{h:02d}:00" for h in range(8, 21)] + [f"{h:02d}:30" for h in range(8, 21)]
        self.time_combo.addItems(times)
        form_layout.addRow("Uhrzeit:", self.time_combo)

        # Dropdown für die Liga (z. B. Landesliga, Kreisoberliga)
        self.league_combo = QtWidgets.QComboBox()
        leagues = self.config.get("leagues", [])
        self.league_combo.addItems(leagues)
        form_layout.addRow("Liga:", self.league_combo)

        # Dropdown für die Altersklasse
        self.age_class_combo = QtWidgets.QComboBox()
        age_classes = self.config.get("age_classes", [])
        self.age_class_combo.addItems(age_classes)
        form_layout.addRow("Altersklasse:", self.age_class_combo)

        # Ergebnisfelder: Heim-Score, Gast-Score und "Other"-Feld
        self.home_score_edit = QtWidgets.QLineEdit()
        self.home_score_edit.setFixedWidth(50)
        self.away_score_edit = QtWidgets.QLineEdit()
        self.away_score_edit.setFixedWidth(50)
        self.other_edit = QtWidgets.QLineEdit()
        result_layout = QtWidgets.QHBoxLayout()
        result_layout.addWidget(QtWidgets.QLabel("Heim-Score:"))
        result_layout.addWidget(self.home_score_edit)
        result_layout.addWidget(QtWidgets.QLabel("Gast-Score:"))
        result_layout.addWidget(self.away_score_edit)
        result_layout.addWidget(QtWidgets.QLabel("Other:"))
        result_layout.addWidget(self.other_edit)
        form_layout.addRow("Ergebnis:", result_layout)

        main_layout.addLayout(form_layout)

        # Button zum Speichern eines Spiels
        self.add_match_button = QtWidgets.QPushButton("Spiel speichern")
        self.add_match_button.clicked.connect(self.add_match)
        main_layout.addWidget(self.add_match_button)

        # Button zum Entfernen eines ausgewählten Eintrags
        self.remove_match_button = QtWidgets.QPushButton("Ausgewählten Eintrag entfernen")
        self.remove_match_button.clicked.connect(self.remove_match)
        main_layout.addWidget(self.remove_match_button)

        # Liste der gespeicherten Spiele
        self.match_list_widget = QtWidgets.QListWidget()
        main_layout.addWidget(self.match_list_widget)

        # Buttons zum Speichern/Laden der Spiel-Liste und Generieren des Spielplans
        buttons_layout = QtWidgets.QHBoxLayout()
        self.save_button = QtWidgets.QPushButton("Liste speichern")
        self.save_button.clicked.connect(self.save_matches)
        self.load_button = QtWidgets.QPushButton("Liste laden")
        self.load_button.clicked.connect(self.load_matches)
        self.generate_button = QtWidgets.QPushButton("Spielplan generieren")
        self.generate_button.clicked.connect(self.generate_graphic)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.load_button)
        buttons_layout.addWidget(self.generate_button)
        main_layout.addLayout(buttons_layout)

        central.setLayout(main_layout)
        self.setCentralWidget(central)
    
    def add_match(self):
        home = self.home_team_edit.text().strip()
        away = self.away_team_edit.text().strip()
        home_suffix = self.home_suffix_edit.text().strip()
        away_suffix = self.away_suffix_edit.text().strip()
        sport = self.sport_combo.currentText()
        day = None
        for rb in self.day_buttons:
            if rb.isChecked():
                day = rb.text()
                break
        time = self.time_combo.currentText()
        league = self.league_combo.currentText()
        age_class = self.age_class_combo.currentText()
        home_score = self.home_score_edit.text().strip()
        away_score = self.away_score_edit.text().strip()
        other = self.other_edit.text().strip()

        if not (home and away and sport):
            QtWidgets.QMessageBox.warning(self, "Eingabefehler", "Bitte Heim, Gast und Sport ausfüllen!")
            return

        match = Match(
            home, home_suffix, away, away_suffix, day, time, league, age_class, sport,
            home_score, away_score, other
        )
        self.matches.append(match)
        self.update_match_list()
        self.clear_form()

    def update_match_list(self):
        self.match_list_widget.clear()
        for match in self.matches:
            display_text = (
                f"{match.day} {match.time} - "
                f"{match.home} {match.home_suffix} ({match.home_score}) vs. "
                f"{match.away} {match.away_suffix} ({match.away_score}) - "
                f"[{match.league} | {match.age_class} | {match.sport}] Other: {match.other}"
            )
            self.match_list_widget.addItem(display_text)

    def remove_match(self):
        current_row = self.match_list_widget.currentRow()
        if current_row >= 0:
            del self.matches[current_row]
            self.update_match_list()

    def clear_form(self):
        self.home_team_edit.clear()
        self.away_team_edit.clear()
        self.home_suffix_edit.clear()
        self.away_suffix_edit.clear()
        self.sport_combo.setCurrentIndex(0)
        self.home_score_edit.clear()
        self.away_score_edit.clear()
        self.other_edit.clear()
        self.day_group.setExclusive(False)
        for rb in self.day_buttons:
            rb.setChecked(False)
        self.day_group.setExclusive(True)
        self.time_combo.setCurrentIndex(0)
        self.league_combo.setCurrentIndex(0)
        self.age_class_combo.setCurrentIndex(0)

    def save_matches(self):
        options = QtWidgets.QFileDialog.Options()
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Liste speichern",
            "",
            "JSON Files (*.json);;All Files (*)",
            options=options,
        )
        if filename:
            try:
                import json
                data = [match.to_dict() for match in self.matches]
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                QtWidgets.QMessageBox.information(self, "Erfolg", "Liste wurde gespeichert.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Fehler", f"Fehler beim Speichern:\n{e}")

    def load_matches(self):
        options = QtWidgets.QFileDialog.Options()
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Liste laden",
            "",
            "JSON Files (*.json);;All Files (*)",
            options=options,
        )
        if filename:
            try:
                import json
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.matches = [Match.from_dict(item) for item in data]
                self.update_match_list()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Fehler", f"Fehler beim Laden:\n{e}")

    def generate_graphic(self):
        options = QtWidgets.QFileDialog.Options()
        base_filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "PNG speichern",
            "",
            "PNG Files (*.png);;All Files (*)",
            options=options,
        )
        if not base_filename:
            QtWidgets.QMessageBox.critical(self, "Fehler", "Fehler beim Erstellen der PNG(s).")
            return

        try:
            generate_match_list_svg(self.matches, base_filename)
            QtWidgets.QMessageBox.information(self, "Erfolg", "PNG(s) wurden erfolgreich erstellt.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Fehler", f"Fehler beim Erstellen der PNG(s): {e}")
