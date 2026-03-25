import random

class Room:
    def __init__(self, description):
        self.description = description
            
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

    def use_item(self, item_name, amount=1):
        if self.inventory.use_item(item_name, amount):
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