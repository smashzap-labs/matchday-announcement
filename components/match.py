class Match:
    def __init__(
        self, home, home_suffix, away, away_suffix, day, time, league, age_class
    ):
        self.home = home
        self.home_suffix = home_suffix
        self.away = away
        self.away_suffix = away_suffix
        self.day = day
        self.time = time
        self.league = league
        self.age_class = age_class

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
            data["league"],
            data["age_class"],
        )
