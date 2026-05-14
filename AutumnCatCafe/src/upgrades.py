"""Upgrade definitions and data."""

class Upgrade:
    def __init__(self, name, base_cost, income_boost, icon_key):
        self.name        = name
        self.base_cost   = base_cost
        self.income_boost= income_boost  # ¥/sec added per level
        self.icon_key    = icon_key
        self.level       = 0
        self._mult       = 1.6           # cost scaling

    # ── computed properties ──────────────────────────────────
    @property
    def current_cost(self):
        return int(self.base_cost * (self._mult ** self.level))

    @property
    def total_income(self):
        return self.income_boost * self.level

    def can_afford(self, yen):
        return yen >= self.current_cost

    def purchase(self):
        self.level += 1


# ── All upgrades (ordered by cost) ──────────────────────────
def make_upgrades():
    return [
        Upgrade("Chochin Lantern",   500,    0.5,  "lantern"),
        Upgrade("Espresso Machine",  2_000,  2.0,  "coffee"),
        Upgrade("More Seating",      5_000,  5.0,  "seat"),
        Upgrade("Premium Beans",     15_000, 15.0, "beans"),
        Upgrade("Lucky Cat Statue",  50_000, 50.0, "cat"),
    ]
