import os, json

def load_config(filename=""):
    if not os.path.exists(filename):
        return 
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def load_teams(filename=""):
    if not os.path.exists(filename):
        return 
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    teams = data.get("teams", [])
    team_dict = {team["name"]: team["logo"] for team in teams}
    team_names = list(team_dict.keys())
    return team_names, team_dict