import random
      
class InventoryItem:
    def __init__(self, name, current, max_stack):
        self.name = name
        self.current = current
        self.max_stack = max_stack

    def use(self, amount=1):
        if self.current >= amount:
            self.current -= amount
            return True
        return False

    def add(self, amount=1):
        self.current = min(self.current + amount, self.max_stack)

    def __str__(self):
        return f"{self.name}: {self.current}/{self.max_stack}"
    
    @staticmethod
    def slump_items():
        randomItems = random.randint(0, 100)
        if randomItems <= 80:
            return random.choice(["bronzeKey", "food", "armorPoints", "healthPotion"])
        elif randomItems <= 60:
            return random.choice(["silverKey"])
        elif randomItems <= 40:
            return random.choice(["goldKey"])
        else:
            return None

class Use:
    def __init__(self, inventory, character):
        self.inventory = inventory
        self.character = character

    def _item(self, item_name, amount=1):
        if self.inventory._item(item_name, amount):
            if item_name == "healthPotion":
                self.character.hp = min(self.character.hp + 20, self.character.max_hp)
                return True
            elif item_name == "food":
                self.character.hp = min(self.character.hp + 10, self.character.max_hp)
                return True
            # Add more effects here
            return True
        return False



class Inventory:
    def __init__(self):
        self.items = {}
        self._load_from_file()

    def _load_from_file(self):
        with open("inventory.txt", "r") as f:
            for line in f.readlines():
                line = line.strip()
                if line:
                    name, amounts = line.split(" - ")
                    current, max_stack = amounts.split("/")
                    self.items[name] = InventoryItem(name, int(current), int(max_stack))

    def save_to_file(self):
        with open("inventory.txt", "w") as f:
            for item in self.items.values():
                f.write(f"{item.name} - {item.current}/{item.max_stack}\n")

    def get_item(self, item_name):
        return self.items.get(item_name)

    def use_item(self, item_name, amount=1):
        if item_name in self.items:
            return self.items[item_name].use(amount)
        return False

    def add_item(self, item_name, amount=1):
        if item_name in self.items:
            self.items[item_name].add(amount)

    def get_all_items(self):
        return self.items

    def display_inventory(self):
        return [str(item) for item in self.items.values()]

class Character:
    def __init__(self, name, hp, attack_power):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack_power = attack_power

    def attack(self, other):
        damage = random.randint(self.attack_power - 2, self.attack_power + 2)
        other.hp -= damage
        return damage

    def is_alive(self):
        return self.hp > 0

    def use_item(self, item_name):
        if item_name == "healthPotion":
            self.hp = min(self.hp + 20, self.max_hp)
            return True
        elif item_name == "food":
            self.hp = min(self.hp + 10, self.max_hp)
            return True
        # Add more items here
        return False


class Enemy(Character):
    """Enemy with preset types and extended stats copied from GUI setup."""

    PRESET_STATS = {
        "slime": {
            "name": "Slime",
            "hp": 30,
            "attack_power": 5,
            "enemy_type": "easy",
            "armor": 0,
            "speed": 4,
            "xp_reward": 10,
            "loot_table": ["food", "bronzeKey"]
        },
        "goblin": {
            "name": "Goblin",
            "hp": 50,
            "attack_power": 7,
            "enemy_type": "easy",
            "armor": 2,
            "speed": 6,
            "xp_reward": 20,
            "loot_table": ["food", "bronzeKey", "armorPoints"]
        },
        "wraith": {
            "name": "Wraith",
            "hp": 80,
            "attack_power": 15,
            "enemy_type": "hard",
            "armor": 4,
            "speed": 8,
            "xp_reward": 45,
            "loot_table": ["silverKey", "healthPotion"]
        },
        "dragon": {
            "name": "Dragon",
            "hp": 200,
            "attack_power": 20,
            "enemy_type": "boss",
            "armor": 10,
            "speed": 5,
            "xp_reward": 100,
            "loot_table": ["goldKey", "armorPoints", "healthPotion"]
        },
    }

    def __init__(self, name, hp, attack_power, enemy_type="generic", armor=0, speed=5, xp_reward=0, loot_table=None):
        super().__init__(name, hp, attack_power)
        self.enemy_type = enemy_type
        self.armor = armor
        self.speed = speed
        self.xp_reward = xp_reward
        self.loot_table = loot_table or []

    @classmethod
    def from_preset(cls, preset_name):
        preset = cls.PRESET_STATS.get(preset_name.lower())
        if not preset:
            raise ValueError(f"Unknown enemy preset: {preset_name}")
        return cls(
            name=preset["name"],
            hp=preset["hp"],
            attack_power=preset["attack_power"],
            enemy_type=preset["enemy_type"],
            armor=preset["armor"],
            speed=preset["speed"],
            xp_reward=preset["xp_reward"],
            loot_table=preset["loot_table"],
        )

    @classmethod
    def get_easy_enemies(cls):
        return [cls.from_preset("slime"), cls.from_preset("goblin")]

    @classmethod
    def get_hard_enemies(cls):
        return [cls.from_preset("wraith")]

    @classmethod
    def get_boss_enemies(cls):
        return [cls.from_preset("dragon")]

    def __str__(self):
        return f"{self.name} ({self.enemy_type.capitalize()}) - HP: {self.hp}/{self.max_hp}, Attack: {self.attack_power}, Armor: {self.armor}, Speed: {self.speed}"

    def is_defeated(self):
        return self.hp <= 0

    def take_damage(self, damage):
        reduced = max(0, damage - self.armor)
        self.hp -= reduced
        return self.hp <= 0

    def attack(self, other):
        damage = random.randint(max(1, self.attack_power - 2), self.attack_power + 2)
        if hasattr(other, "take_damage"):
            other.take_damage(damage)
        else:
            other.hp -= damage
        return damage

    def drop_loot(self):
        if self.loot_table:
            return random.choice(self.loot_table)
        return InventoryItem.slump_items()

    def taunt(self):
        return f"{self.name} ({self.enemy_type}) snarls at you!"
   