import random

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

# class enemy:
#     def __init__(self, name, hp, attack_power):
#         self.name = name
#         self.hp = hp
#         self.max_hp = hp
#         self.attack_power = attack_power

#     def attack(self):

        