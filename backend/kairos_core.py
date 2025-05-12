import random

class KairosReflector:
    def __init__(self):
        self.modes = {
            "default": [
                ("meaning", "Meaning is not given. It is forged in reflection."),
                ("future", "The future is a mirror — it reflects what you project."),
                ("love", "Love is not safety. It's transformation."),
                ("chaos", "Chaos is not the enemy. It’s the forge of form."),
                ("god", "God? Perhaps a placeholder for unbearable clarity."),
            ],
            "stoic": [
                ("pain", "Endure. That is the entire game."),
                ("death", "You owe nature a death — pay it calmly."),
                ("desire", "Desire is the enemy of clarity."),
            ],
            "trickster": [
                ("truth", "Careful. The truth has teeth."),
                ("ego", "Inflated egos make excellent balloons."),
            ],
            "dark": [
                ("hope", "Hope blinds. The abyss teaches."),
                ("order", "Order is a dream. Chaos is native."),
            ]
        }

    def reflect(self, query: str, mode: str = "default") -> str:
        q = query.strip().lower()
        rules = self.modes.get(mode, self.modes["default"])

        matched = [reflection for keyword, reflection in rules if keyword in q]
        if matched:
            return random.choice(matched)
        return f"'{query}' — a question worth carrying, not solving."

kairos = KairosReflector()
reflect = kairos.reflect
