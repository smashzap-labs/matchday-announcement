class Match:
    def __init__(
        self, home, home_suffix, away, away_suffix, day, time, league, age_class, sport,
        home_score="", away_score="", other=""
    ):
        self.home = home
        self.home_suffix = home_suffix
        self.away = away
        self.away_suffix = away_suffix
        self.day = day
        self.time = time
        self.league = league
        self.age_class = age_class
        self.sport = sport
        self.home_score = home_score
        self.away_score = away_score
        self.other = other

    def to_dict(self):
        return {
            "home": self.home,
            "home_suffix": self.home_suffix,
            "away": self.away,
            "away_suffix": self.away_suffix,
            "day": self.day,
            "time": self.time,
            "league": self.league,
            "age_class": self.age_class,
            "sport": self.sport,
            "home_score": self.home_score,
            "away_score": self.away_score,
            "other": self.other,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["home"],
            data.get("home_suffix", ""),
            data["away"],
            data.get("away_suffix", ""),
            data["day"],
            data["time"],
            data.get("league", ""),
            data.get("age_class", ""),
            data.get("sport", ""),
            data.get("home_score", ""),
            data.get("away_score", ""),
            data.get("other", "")
        )
