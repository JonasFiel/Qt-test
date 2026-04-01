import random
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QTextEdit
from engine import Character, Inventory, InventoryItem, Use, Enemy  #Importerar saker från engine.py
from PySide6.QtCore import QTimer


class RPGWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Py Dungeon")

        # Initialize Game Data
        self.player = Character("Hero", 100, 10, 5, 0)
        self.inventory = Inventory()
        self.use_item_handler = Use(self.inventory, self.player)

        # Define enemies using the Enemy class from engine
        self.enemies_easy = Enemy.get_easy_enemies()
        self.enemies_hard = Enemy.get_hard_enemies()
        self.enemies_boss = Enemy.get_boss_enemies()

        self.current_enemy = None

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
            item_name = InventoryItem.slump_items()
            if item_name:
                self.log.append(f"You found a {item_name}!")
                self.inventory.add_item(item_name, 1)
            else:
                self.log.append("You found nothing of value.")
        else:
            self.log.append("You found nothing of value.")

    def check_for_enemy(self):
        self.enemy_chance = random.randint(0, 100)
        if self.enemy_chance <= 80:
            self.current_enemy = random.choice(self.enemies_easy)
            self.log.append(self.current_enemy.taunt())
            QTimer.singleShot(1000, self.fight_ui)
        else:
            for btn in self.buttons:
                btn.setEnabled(True)



    def fight_ui(self):
        if not self.current_enemy:
            return
        self.label_hp = QLabel(f"Player HP: {self.player.hp} | {self.current_enemy.name} HP: {self.current_enemy.hp}")
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.btn_attack = QPushButton("Attack Enemy")
        self.btn_use_item = QPushButton("Use Item")
        
        self.btn_attack.clicked.connect(self.do_combat_round)
        self.btn_use_item.clicked.connect(self.use_item)

        self.inventory_label = QLabel("Inventory:")
        self.inventory_list = QLabel("\n".join([str(item) for item in self.inventory.get_all_items().values()]))  # Display inventory items

        self.use_item_ui = Use(self.inventory, self.player)  # Create an instance of the Use class to handle item usage


        # Combat log message
        self.log.append("A battle begins!")
        self.log.append(self.current_enemy.taunt())

        # Layout for combat elements
        combat_layout = QVBoxLayout()
        combat_layout.addWidget(self.label_hp)
        combat_layout.addWidget(self.log)
        combat_layout.addWidget(self.btn_attack)
        combat_layout.addWidget(self.btn_use_item)

        # Layout for inventory
        inventory_layout = QVBoxLayout()
        inventory_layout.addWidget(self.inventory_label)
        inventory_layout.addWidget(self.inventory_list)

        # Main horizontal layout
        main_layout = QHBoxLayout()
        main_layout.addLayout(inventory_layout)
        main_layout.addLayout(combat_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def use_item(self):
        if self.use_item_handler.use_item("healthPotion", 1):
            self.log.append("You used a health potion! You feel rejuvenated! Your HP has been restored by 20 points.")
            if self.current_enemy:
                self.label_hp.setText(f"Player HP: {self.player.hp} | {self.current_enemy.name} HP: {self.current_enemy.hp}")
            else:
                self.label_hp.setText(f"Player HP: {self.player.hp}")
        else:
            self.log.append("You don't have any health potions left!")

    def do_combat_round(self):
        if not self.current_enemy:
            return

        dmg = self.player.attack(self.current_enemy)
        self.log.append(f"You hit {self.current_enemy.name} for {dmg} damage!")

        if self.current_enemy.is_defeated():
            self.log.append("The enemy is defeated!")
            loot = self.current_enemy.drop_loot()
            if loot:
                self.log.append(f"You found a {loot}!")
                self.inventory.add_item(loot, 1)
            self.btn_attack.setEnabled(False)
            self.btn_use_item.setEnabled(False)

            #Resets the enemies hp after the battle so that they are ready for the next fight
            self.current_enemy.reset_hp()

            self.current_enemy = None
            QTimer.singleShot(2000, self.setup_ui)
            return
        

        dmg_enemy = self.current_enemy.attack(self.player)
        self.log.append(f"{self.current_enemy.name} hits you for {dmg_enemy} damage!")

        if not self.player.is_alive():
            self.log.append("You have been defeated! Game Over.")
            self.btn_attack.setEnabled(False)
            self.btn_use_item.setEnabled(False)

        self.label_hp.setText(f"Player HP: {self.player.hp} | {self.current_enemy.name} HP: {self.current_enemy.hp}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RPGWindow()
    window.show()
    sys.exit(app.exec())