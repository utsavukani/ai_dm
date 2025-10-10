import json
from typing import Dict, List


class CharacterSheet:
    """Player character tracking system"""

    def __init__(self):
        self.stats = {
            'name': 'Adventurer',
            'level': 1,
            'health': 100,
            'max_health': 100,
            'experience': 0,
            'gold': 50,
            'strength': 10,
            'intelligence': 10,
            'charisma': 10
        }
        self.inventory = ['Basic Sword', 'Leather Armor', 'Health Potion']
        self.abilities = ['Combat Training']
        self.status_effects = []

    def add_item(self, item: str):
        """Add item to inventory"""
        if item and item not in self.inventory:
            self.inventory.append(item)
            return f"Added {item} to inventory!"
        return f"{item} already in inventory."

    def remove_item(self, item: str):
        """Remove item from inventory"""
        if item in self.inventory:
            self.inventory.remove(item)
            return f"Removed {item} from inventory."
        return f"{item} not found in inventory."

    def gain_experience(self, xp: int):
        """Add experience points"""
        self.stats['experience'] += xp
        old_level = self.stats['level']

        # Level up check
        while self.stats['experience'] >= self.stats['level'] * 100:
            self.level_up()

        if self.stats['level'] > old_level:
            return f"Gained {xp} XP! Level up! Now level {self.stats['level']}"
        return f"Gained {xp} experience points."

    def level_up(self):
        """Level up character"""
        self.stats['level'] += 1
        self.stats['max_health'] += 20
        # Full heal on level up
        self.stats['health'] = self.stats['max_health']
        self.stats['strength'] += 2
        self.stats['intelligence'] += 2
        self.stats['charisma'] += 1

    def take_damage(self, damage: int):
        """Apply damage to character"""
        self.stats['health'] = max(0, self.stats['health'] - damage)
        if self.stats['health'] == 0:
            return "You have fallen unconscious!"
        return f"Took {damage} damage. Health: {self.stats['health']}/{self.stats['max_health']}"

    def heal(self, amount: int):
        """Heal character"""
        old_health = self.stats['health']
        self.stats['health'] = min(
            self.stats['max_health'], self.stats['health'] + amount)
        healed = self.stats['health'] - old_health
        return f"Healed {healed} HP. Health: {self.stats['health']}/{self.stats['max_health']}"

    def display_sheet(self):
        """Display character information"""
        print(f"\n{'='*30}")
        print(f"CHARACTER SHEET")
        print(f"{'='*30}")
        print(f"Name: {self.stats['name']}")
        print(
            f"Level: {self.stats['level']} (XP: {self.stats['experience']}/{self.stats['level'] * 100})")
        print(f"Health: {self.stats['health']}/{self.stats['max_health']}")
        print(f"Gold: {self.stats['gold']}")
        print(f"\nAttributes:")
        print(f"  Strength: {self.stats['strength']}")
        print(f"  Intelligence: {self.stats['intelligence']}")
        print(f"  Charisma: {self.stats['charisma']}")
        print(f"\nInventory ({len(self.inventory)} items):")
        for item in self.inventory:
            print(f"  - {item}")
        print(f"\nAbilities:")
        for ability in self.abilities:
            print(f"  - {ability}")
        if self.status_effects:
            print(f"\nStatus Effects:")
            for effect in self.status_effects:
                print(f"  - {effect}")
        print(f"{'='*30}")

    def to_dict(self) -> Dict:
        """Convert to dictionary for saving"""
        return {
            'stats': self.stats,
            'inventory': self.inventory,
            'abilities': self.abilities,
            'status_effects': self.status_effects
        }

    def from_dict(self, data: Dict):
        """Load from dictionary"""
        self.stats = data.get('stats', self.stats)
        self.inventory = data.get('inventory', self.inventory)
        self.abilities = data.get('abilities', self.abilities)
        self.status_effects = data.get('status_effects', self.status_effects)
