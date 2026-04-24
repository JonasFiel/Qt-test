import random
      
# Representerar ett item i inventoryt
class InventoryItem:
    #Representerar ett enskilt föremål i spelarens inventory.
    #Hanterar namn, aktuell mängd och max stackstorlek.
    def __init__(self, name, current, max_stack):
        #Initierar ett InventoryItem med namn, aktuell mängd och max stack.
        self.name = name
        self.current = current
        self.max_stack = max_stack

    def use(self, amount=1):
        # Använder en viss mängd av föremålet om möjligt. Returnerar True om lyckat.
        if self.current >= amount:
            self.current -= amount
            return True
        return False

    def add(self, amount=1):
        # Lägger till en viss mängd till föremålet, upp till max stack.
        self.current = min(self.current + amount, self.max_stack)

    def __str__(self):
        # Returnerar en strängrepresentation av föremålet.
        return f"{self.name}: {self.current}/{self.max_stack}"
    
    # Slumpa ett random item
    @staticmethod
    def slump_items():
        # Slumpar ett slumpmässigt föremål baserat på sannolikheter.
        randomItems = random.randint(0, 100)
        if randomItems <= 80:
            return random.choice(["Bronze Key", "Food", "Health Potion"])
        elif randomItems <= 60:
            return random.choice(["Silver Key", "Shield scroll"])
        elif randomItems <= 40:
            return random.choice(["Gold Key"])
        else:
            return None


# Hanterar användning av items
class Use:
    #Hanterar användning av föremål från inventoryt och applicerar deras effekter på karaktären.
    #Till exempel återställer hälsa från potions eller mat.
    def __init__(self, inventory, character):
        #Initierar Use med inventory och character för att hantera item-användning.
        self.inventory = inventory
        self.character = character

    # Använd ett item och applicera effekten
    def use_item(self, item_name, amount=1):
        #Använder ett item från inventoryt och applicerar dess effekt på karaktären.
        if self.inventory.use_item(item_name, amount):
            if item_name == "Health Potion":
                self.character.hp = min(self.character.hp + 20, self.character.max_hp)
                return True
            elif item_name == "Food":
                self.character.hp = min(self.character.hp + 10, self.character.max_hp)
                return True
            return True
        return False



# Hanterar spelarens inventorium
class Inventory:
    #Hanterar spelarens inventory, inklusive laddning från och sparande till fil.
    #Tillåter att lägga till, använda och hämta föremål.
    def __init__(self):
        #Initierar Inventory och laddar från fil.
        self.items = {}
        self._load_from_file()

    # Läs inventoryt från fil
    def _load_from_file(self):
        #Laddar inventory från 'inventory.txt'.
        with open("inventory.txt", "r") as f:
            for line in f.readlines():
                line = line.strip()
                if line:
                    name, amounts = line.split(" - ")
                    current, max_stack = amounts.split("/")
                    self.items[name] = InventoryItem(name, int(current), int(max_stack))

    # Spara inventoryt till fil
    def save_to_file(self):
        #Sparar inventory till 'inventory.txt'.
        with open("inventory.txt", "w") as f:
            for item in self.items.values():
                f.write(f"{item.name} - {item.current}/{item.max_stack}\n")

    def get_item(self, item_name):
        #Hämtar ett specifikt item från inventoryt.
        return self.items.get(item_name)

    def use_item(self, item_name, amount=1):
        #Använder ett item från inventoryt.
        if item_name in self.items:
            return self.items[item_name].use(amount)
        return False

    def add_item(self, item_name, amount=1):
        #Lägger till ett item till inventoryt.
        if item_name not in self.items:
            self.items[item_name] = InventoryItem(item_name, 0, 10)
        self.items[item_name].add(amount)

    def get_all_items(self):
        #Returnerar alla items i inventoryt.
        return self.items

    def display_inventory(self):
        #Returnerar en lista av strängrepresentationer av alla items.
        return [str(item) for item in self.items.values()]

# Representerar en karaktär (spelare eller fiende)
class Character:
    #Basklass för spelkaraktärer, inklusive spelare och fiender.
    #Hanterar grundläggande egenskaper som HP, attack, speed och armor (sp).
    #Inkluderar metoder för att attackera, ta skada och undvika attacker.
    def __init__(self, name, hp, attack_power, speed=5, sp=0):
        #Initierar en Character med namn, HP, attack, speed och armor (sp).
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack_power = attack_power
        self.speed = speed
        self.sp = sp

    def attack(self, other):
        #Utför en attack mot en annan karaktär, kontrollerar dodge och returnerar skada.
        # Check if other dodges
        dodge_roll = random.randint(1, 100)
        if dodge_roll <= other.dodge_chance():
            return 0  # Dodged
        damage = random.randint(self.attack_power - 2, self.attack_power + 2)
        
        if hasattr(other, "take_damage"):
            actual_damage = other.take_damage(damage)
        else:
            other.hp -= damage
            actual_damage = damage
        return actual_damage
    
    def take_damage(self, damage):
        #Tar skada, reducerad av armor, och returnerar faktisk skada.
        reduced = max(0, damage - self.sp)
        self.hp -= reduced
        return reduced

    def dodge_chance(self):
        #Beräknar dodge-chans baserat på speed, max 50%.
        # Dodge chance scales with speed and is capped to prevent extreme values.
        return min(50, max(0, self.speed * 5))
    
    # Kontrollera om karaktären är vid liv
    def is_alive(self):
        #Returnerar True om karaktären har HP kvar.
        return self.hp > 0

    # Återställ HP till max
    def reset_hp(self):
        #Återställer HP till maxvärde.
        self.hp = self.max_hp


# Representerar en fiende
class Enemy(Character):
    
    #Underklass till Character som representerar fiender i spelet.
    #Har fördefinierade typer (slime, goblin, etc.) med specifika stats och loot-tabeller.
    #Kan skapa fiender från presets och hantera deras unika beteenden som loot-drop och taunts.
    
    PRESET_STATS = {
        "slime": {
            "name": "Slime",
            "hp": 30,
            "attack_power": 5,
            "enemy_type": "easy",
            "sp": 0,
            "speed": 4,
            "coins": random.randint(5, 10),
            "loot_table": ["Food", "Bronze Key"]
        },
        "goblin": {
            "name": "Goblin",
            "hp": 50,
            "attack_power": 7,
            "enemy_type": "easy",
            "sp": 2,
            "speed": 6,
            "coins": random.randint(15, 25),
            "loot_table": ["Food", "Bronze Key", "Shield scroll"]
        },
        "wraith": {
            "name": "Wraith",
            "hp": 80,
            "attack_power": 15,
            "enemy_type": "hard",
            "sp": 4,
            "speed": 8,
            "coins": random.randint(35, 45),
            "loot_table": ["Silver Key", "Health Potion"]
        },
        "dragon": {
            "name": "Dragon",
            "hp": 200,
            "attack_power": 20,
            "enemy_type": "boss",
            "sp": 10,
            "speed": 5,
            "coins": random.randint(90, 110),
            "loot_table": ["Gold Key", "Shield scroll", "Health Potion"]
        },
    }

    def __init__(self, name, hp, attack_power, enemy_type="generic", sp=0, speed=5, coins=0, loot_table=None):
        #Initierar en Enemy med namn, stats, typ, coins och loot-table.
        super().__init__(name, hp, attack_power)
        self.enemy_type = enemy_type
        self.sp = sp
        self.speed = speed
        self.coins = coins
        self.loot_table = loot_table or []

    # Skapa en fiende från fördefinierade statistik
    @classmethod
    def from_preset(cls, preset_name):
        #Skapar en Enemy från en fördefinierad preset.
        preset = cls.PRESET_STATS.get(preset_name.lower())
        if not preset:
            raise ValueError(f"Unknown enemy preset: {preset_name}")
        return cls(
            name=preset["name"],
            hp=preset["hp"],
            attack_power=preset["attack_power"],
            enemy_type=preset["enemy_type"],
            sp=preset["sp"],
            speed=preset["speed"],
            coins=preset["coins"],
            loot_table=preset["loot_table"],
        )

    # Returnera låta fiender
    @classmethod
    def get_easy_enemies(cls):
        #Returnerar en lista av enkla fiender.
        return [cls.from_preset("slime"), cls.from_preset("goblin")]

    @classmethod
    def get_hard_enemies(cls):
        #Returnerar en lista av svåra fiender.
        return [cls.from_preset("wraith")]

    @classmethod
    def get_boss_enemies(cls):
        #Returnerar en lista av boss-fiender.
        return [cls.from_preset("dragon")]

    def __str__(self):
        #Returnerar en strängrepresentation av fienden.
        return f"{self.name} ({self.enemy_type.capitalize()}) - HP: {self.hp}/{self.max_hp}, Attack: {self.attack_power}, sp: {self.sp}, Speed: {self.speed}"

    def is_defeated(self):
        #Returnerar True om fienden är besegrad.
        return self.hp <= 0

    def take_damage(self, damage):
        #Tar skada och returnerar faktisk skada.
        reduced = max(0, damage - self.sp)
        self.hp -= reduced
        return reduced

    def attack(self, other):
        #Utför en attack mot spelaren, kontrollerar dodge.
        # Check if other dodges
        dodge_roll = random.randint(1, 100)
        if dodge_roll <= other.dodge_chance():
            return 0  # Dodged
        damage = random.randint(max(1, self.attack_power - 2), self.attack_power + 2)
        if hasattr(other, "take_damage"):
            actual_damage = other.take_damage(damage)
        else:
            other.hp -= damage
            actual_damage = damage
        return actual_damage

    # Fienden släpper ett byte
    def drop_loot(self):
        #Släpper loot från fiendens loot-table eller slumpmässigt.
        if self.loot_table:
            return random.choice(self.loot_table)
        return InventoryItem.slump_items()

    # Fienden hotar spelaren
    def taunt(self):
        #Returnerar en taunt-sträng från fienden.
        return f"{self.name} ({self.enemy_type}) snarls at you!"
