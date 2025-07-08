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
        def s(v, max_length=25):
            if isinstance(v, str) and len(v) > max_length:
                return v[:max_length - 3] + "..."
            return v

        return cls(
            s(data["home"]),
            s(data.get("home_suffix", "")),
            s(data["away"]),
            s(data.get("away_suffix", "")),
            s(data.get("day", "")),
            s(data.get("time", "")),
            s(data.get("league", "")),
            s(data.get("age_class", "")),
            s(data["sport"]),
            s(data.get("home_score", "")),
            s(data.get("away_score", "")),
            s(data.get("other", ""))
        )
