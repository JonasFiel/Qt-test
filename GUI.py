import random
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QTextEdit
from engine import Character, Inventory, InventoryItem, Room  #Importerar saker från engine.py
from PySide6.QtCore import QTimer


class RPGWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Py Dungeon")

        # Initialize Game Data
        self.player = Character("Hero", 100, 10)
        self.inventory = Inventory()

        self.enemy_slime = Character("Slime", 30, 5)
        self.enemy_goblin = Character("Goblin", 50, 7)
        self.enemy_dragon = Character("Dragon", 200, 20)
        self.enemy_wraith = Character("Wraith", 80, 15)

        enemiesAll = [self.enemy_slime, self.enemy_goblin, self.enemy_dragon, self.enemy_wraith]
        enemiesEasy = [self.enemy_slime, self.enemy_goblin]
        enemiesHard = [self.enemy_wraith]
        enemiesBoss = [self.enemy_dragon]

        self.enemyeasy = random.choice(enemiesEasy)  # Randomly select an enemy for the player to fight when going north

        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        self.label = QLabel("You are a solo adventurer who has entered the py dungeon. What do you do?")
        self.label.setWordWrap(True) # Allow text to wrap for better readability
        self.log = QTextEdit()
        self.log.setReadOnly(True) # Make the log read-only so players can't type in it

        self.inventory_label = QLabel("Inventory:")
        self.inventory_list = QLabel("\n".join([str(item) for item in self.inventory.get_all_items().values()]))  # Display inventory items

        self.btn_north = QPushButton("Go North")
        self.btn_south = QPushButton("Go South")
        self.btn_east = QPushButton("Go East")
        self.btn_west = QPushButton("Go West")

        self.btn_north.clicked.connect(self.room)
        self.btn_south.clicked.connect(self.room)
        self.btn_east.clicked.connect(self.room)
        self.btn_west.clicked.connect(self.room)

        # room_chance = random.randint(0, 100)
        # if room_chance <= 50:
        #     self.log.append("You see a door to the north. It looks like it leads to another room.")
        # if room_chance <= 20:
        #     # Need a bronze key to enter this room
        #     self.log.append("You see a door to the north, but it is locked. You need a Bronze Key to enter.")
        #     self.btn_north.setEnabled(False)  # Disable the north button until the player finds a Bronze Key
        # elif room_chance <= 40:
        #     # Need a silver key to enter this room
        #     self.log.append("You see a door to the north, but it is locked. You need a Silver Key to enter.")
        #     self.btn_north.setEnabled(False)  # Disable the north button until the player finds a Silver Key
        # elif room_chance <= 60:
        #     # Need a golden key to enter this room
        #     self.log.append("You see a door to the north, but it is locked. You need a Golden Key to enter.")
        #     self.btn_north.setEnabled(False)  # Disable the north button until the player finds a Golden Key


        self.buttons = [self.btn_north, self.btn_south, self.btn_east, self.btn_west]
        for btn in self.buttons:
            btn.setFixedWidth(100)  # Set a fixed width for all buttons for better UI consistency

        inventory_layout = QVBoxLayout()
        inventory_layout.addWidget(self.inventory_label)
        inventory_layout.addWidget(self.inventory_list)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.btn_north)
        button_layout.addWidget(self.btn_south)
        button_layout.addWidget(self.btn_east)
        button_layout.addWidget(self.btn_west)

        label_layout = QVBoxLayout()
        label_layout.addWidget(self.label)
        label_layout.addWidget(self.log)

        layout = QHBoxLayout()
        layout.addLayout(inventory_layout)
        layout.addLayout(label_layout)
        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def room(self):
        
        for btn in self.buttons:
            btn.setEnabled(False)  # Disable all buttons to prevent multiple clicks while processing the room event

        self.random_description = random.choice(["a dimly lit cave.", "a damp prison cell.", "a deep pit.", "a small mossy room."])
        self.log.append(f"You entered {self.random_description}.")
        
        # Show item message after 1 second
        QTimer.singleShot(1000, self.show_item_message)
        
        # Check for enemy after 2.5 seconds
        QTimer.singleShot(2500, self.check_for_enemy)

    def show_item_message(self):
        self.item_chance = random.randint(0, 100)
        if self.item_chance <= 50:
            self.RandomItem = random.choice(list(self.inventory.get_all_items().values()))
            self.log.append(f"You found a {self.RandomItem.name}!")
            self.inventory.add_item(self.RandomItem.name, 1)
        else:
            self.log.append("You found nothing of value.")

    def check_for_enemy(self):
        self.enemy_chance = random.randint(0, 100)
        if self.enemy_chance <= 80:
            self.enemy = random.choice([self.enemyeasy])
            self.log.append(f"An enemy approaches: {self.enemy.name}!")
            QTimer.singleShot(1000, self.fight_ui)
        else:
            for btn in self.buttons:
                btn.setEnabled(True)



    def fight_ui(self):
        self.label_hp = QLabel(f"Player HP: {self.player.hp} | {self.enemy.name} HP: {self.enemy.hp}")
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.btn_attack = QPushButton("Attack Enemy")
        
        self.btn_attack.clicked.connect(self.do_combat_round)

        layout = QVBoxLayout()
        layout.addWidget(self.label_hp)
        layout.addWidget(self.log)
        layout.addWidget(self.btn_attack)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def do_combat_round(self):
        # Så att spelaren attackerar enemy
        dmg = self.player.attack(self.enemy)
        self.log.append(f"You hit {self.enemy.name} for {dmg} damage!")
        
        # Enemy attackerar spelaren när man attackerar den
        dmg_enemy = self.enemy.attack(self.player)
        self.log.append(f"{self.enemy.name} hits you for {dmg_enemy} damage!")

        if not self.enemy.is_alive():
            self.log.append("The enemy is defeated!")
            self.RandomItem = random.choice(list(self.inventory.get_all_items().values()))
            self.log.append(f"You found a {self.RandomItem.name}!")
            self.inventory.add_item(self.RandomItem.name, 1)
            self.btn_attack.setEnabled(False)  #Gör så att attack inte gör något

            QTimer.singleShot(2000, self.setup_ui)  # Gå tillbaka till huvud UI efter 2 sekunder
        elif not self.player.is_alive():
            self.log.append("You have been defeated! Game Over.")
            self.btn_attack.setEnabled(False)
        
        # Update HP display
        self.label_hp.setText(f"Player HP: {self.player.hp} / {self.enemy.name} HP: {self.enemy.hp}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RPGWindow()
    window.show()
    sys.exit(app.exec())