import random

class Room:
    def __init__(self, description):
        self.description = description
        self.characters = []
            
    def add_exit(self, direction, room):
        self.exits = {}
        self.direktions = ["North", "South", "East", "West"]
        for direction in self.direktions:
            self.origin = [self.direktions - 2]
            for i in range(4):
                self.exit = random.choice(self.direktions)
                if self.exit == self.origin:
                    self.exit = None
                else:
                    self.exits.append(self.exit)

        self.direction = direction

    def add_character(self, character):
        self.characters.append(character)
        
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
    
    def slump_items(self, items):
        self.items = items
        self.randomItems = random.randint(0, 100)
        if self.randomItems <= 80:
            self.commonRandom = random.choice(self.commonItems)
            self.commonItems = ["Bronze Key"]
        elif self.randomItems <= 60:
            self.rareRandom = random.choice(self.rareItems)
            self.rareItems = ["Silver Key"]
        elif self.randomItems <= 40:
            self.legRandom = random.choice(self.legItems)
            self.legItems = ["Golden Key"]
        else:
            self.items = None


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