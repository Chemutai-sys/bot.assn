class CryptoBuddy:
    def __init__(self, name="CryptoBuddy", tone="friendly"):
        self.name = name
        self.tone = tone

        # --- 2) Predefined Crypto Data (scores are 0..1) ---
        self.crypto_db = {
            "Bitcoin": {
                "price_trend": "rising",
                "market_cap": "high",
                "energy_use": "high",
                "sustainability_score": 3/10  # 0.3
            },
            "Ethereum": {
                "price_trend": "stable",
                "market_cap": "high",
                "energy_use": "medium",
                "sustainability_score": 6/10  # 0.6
            },
            "Cardano": {
                "price_trend": "rising",
                "market_cap": "medium",
                "energy_use": "low",
                "sustainability_score": 8/10  # 0.8
            },
        }

    # --- 1) Personality helpers ---
    def greet(self):
        if self.tone == "meme":
            return f"Yo! I’m {self.name} 🧠💸—let’s hunt green candles and clean energy!"
        elif self.tone == "professional":
            return f"Hello, I’m {self.name}. How can I assist with your crypto query today?"
        return f"Hey there! I’m {self.name}. Let’s find you a green and growing crypto! 🌱📈"

    # --- Utility scoring for advice rules ---
    def _trend_weight(self, t):
        return {"rising": 2, "stable": 1, "falling": 0}.get(t, 0)

    def _mcap_weight(self, m):
        return {"high": 2, "medium": 1, "low": 0}.get(m, 0)

    # --- 3 & 4) Core logic + advice rules ---
    def trending_up(self):
        return [c for c, v in self.crypto_db.items() if v["price_trend"] == "rising"]

    def most_sustainable(self):
        # Primary: highest sustainability_score; tie-breaker: lower energy_use
        energy_rank = {"low": 2, "medium": 1, "high": 0}
        return max(
            self.crypto_db,
            key=lambda c: (self.crypto_db[c]["sustainability_score"],
                           energy_rank[self.crypto_db[c]["energy_use"]])
        )

    def recommend_profitable(self):
        # Profitability rule: prioritize rising trend + high market cap
        # Tie-break with sustainability_score
        return max(
            self.crypto_db,
            key=lambda c: (
                self._trend_weight(self.crypto_db[c]["price_trend"]),
                self._mcap_weight(self.crypto_db[c]["market_cap"]),
                self.crypto_db[c]["sustainability_score"]
            )
        )

    def recommend_sustainable(self):
        # Sustainability rule: energy_use == low AND score >= 0.7; else fallback to most_sustainable
        candidates = [
            c for c, v in self.crypto_db.items()
            if v["energy_use"] == "low" and v["sustainability_score"] >= 0.7
        ]
        return candidates[0] if candidates else self.most_sustainable()

    def _fmt_coin_line(self, coin):
        v = self.crypto_db[coin]
        score10 = int(round(v["sustainability_score"] * 10))
        return (f"{coin}: trend={v['price_trend']}, mcap={v['market_cap']}, "
                f"energy={v['energy_use']}, sustainability={score10}/10")

    # --- Natural-language router ---
    def respond(self, user_query: str) -> str:
        q = user_query.lower().strip()

        # small talk / meta
        if q in {"hi", "hello", "hey"}:
            return self.greet()
        if "name" in q:
            return f"My name is {self.name}."
        if q in {"help", "menu"} or "help" in q:
            return (
                "Try asking:\n"
                "- Which crypto is trending up?\n"
                "- What’s the most sustainable coin?\n"
                "- Which coin is most profitable right now?\n"
                "- Show me the data / list\n"
                "Type quit/exit to leave."
            )

        # sustainability-focused
        if any(w in q for w in ("sustain", "green", "eco", "environment")):
            pick = self.recommend_sustainable()
            return f"Invest in {pick}! 🌱 It’s eco-friendlier and has long-term potential.\n" + self._fmt_coin_line(pick)

        # trending up
        if any(w in q for w in ("trend", "trending", "rising", "going up", "up")):
            ups = self.trending_up()
            if ups:
                lines = "\n".join(self._fmt_coin_line(c) for c in ups)
                return f"Trending up right now: {', '.join(ups)} 📈\n{lines}"
            return "No coins are trending up at the moment."

        # profitability-focused
        if any(w in q for w in ("profit", "profitable", "best", "invest")):
            pick = self.recommend_profitable()
            return f"Based on trend and market cap, consider {pick} for profitability. 💡\n" + self._fmt_coin_line(pick)

        # energy questions
        if "energy" in q:
            by_energy = sorted(self.crypto_db, key=lambda c: {"low":0,"medium":1,"high":2}[self.crypto_db[c]["energy_use"]])
            lines = "\n".join(self._fmt_coin_line(c) for c in by_energy)
            return "Lowest energy use first:\n" + lines

        # list/show data
        if any(w in q for w in ("list", "show", "data", "dataset")):
            lines = "\n".join(self._fmt_coin_line(c) for c in self.crypto_db)
            return "Here’s the current dataset:\n" + lines

        return "I’m not sure yet—try 'help'. (Reminder: this is a toy demo, not financial advice.)"

# --- 5) Test your bot (interactive loop) ---
if __name__ == "__main__":
    bot = CryptoBuddy(name="CryptoBuddy", tone="friendly")
    print(bot.greet())
    while True:
        try:
            user = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print(f"\n{bot.name}: Goodbye!")
            break
        if user.lower().strip() in {"quit", "exit"}:
            print(f"{bot.name}: Goodbye!")
            break
        print(f"{bot.name}:", bot.respond(user))