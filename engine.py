import random

class Room:
    def __init__(self, description):
        self.description = description
        self.exits = {}
        self.characters = []

    def add_exit(self, direction, room):
        self.exits[direction] = room

    def add_character(self, character):
        self.characters.append(character)
        
class Inventory(self):  
    def __init__(self):
        with open("inventory.txt", "r") as f:
            self.items = [line.strip() for line in f.readlines()]

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