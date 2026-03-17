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

        self.enemy = random.choice(enemiesEasy)  # Randomly select an enemy for the player to fight when going north

        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        self.label = QLabel("You are a solo adventurer who has entered the py dungeon. What do you do?")
        self.label.setWordWrap(True) # Allow text to wrap for better readability
        self.log = QTextEdit()
        self.log.setReadOnly(True) # Make the log read-only so players can't type in it

        self.btn_north = QPushButton("Go North")
        self.btn_south = QPushButton("Go South")
        self.btn_east = QPushButton("Go East")
        self.btn_west = QPushButton("Go West")

        self.btn_north.clicked.connect(self.fight_ui)
        self.btn_south.clicked.connect(self.fight_ui)
        self.btn_east.clicked.connect(self.fight_ui)
        self.btn_west.clicked.connect(self.fight_ui)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.btn_north)
        button_layout.addWidget(self.btn_south)
        button_layout.addWidget(self.btn_east)
        button_layout.addWidget(self.btn_west)

        label_layout = QVBoxLayout()
        label_layout.addWidget(self.label)
        label_layout.addWidget(self.log)

        layout = QHBoxLayout()
        layout.addLayout(label_layout)
        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


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
            self.btn_attack.setEnabled(False)  # Disable attack button after defeating the enemy
            self.wait_timer = QTimer()
            self.wait_timer.timeout.connect(self.setup_ui)  # Return to main UI after waiting
            self.wait_timer.start(2000)  # Wait 2 seconds before returning to main UI
        elif not self.player.is_alive():
            self.log.append("You have been defeated! Game Over.")
            self.btn_attack.setEnabled(False)
        
        # Update HP display
        self.label_hp.setText(f"Player HP: {self.player.hp} | {self.enemy.name} HP: {self.enemy.hp}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RPGWindow()
    window.show()
    sys.exit(app.exec())
