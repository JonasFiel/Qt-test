import random
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QTextEdit #importerar saker från pyside6
from engine import Character, Inventory, InventoryItem, Use, Enemy #Importerar klasser från engine.py
from PySide6.QtCore import QTimer

# detta är den grafiska delen av spelet, där vi skapar fönstret, knapparna, och all interaktion med användaren. Vi använder klasserna från engine.py för att hantera spelets logik och data.
class RPGWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Py Dungeon") #Titel på fönstret

        self.player = Character("Hero", 100, 10, 5, 0) #Skapar en spelare med namn, hp, attack power, speed och armor
        self.inventory = Inventory() #Skapar en inventory instans för spelaren
        self.inventory.add_item("Food", 1) #Lägger till en mat i inventoryt så att spelaren har något att börja med
        self.use_item_handler = Use(self.inventory, self.player) #Skapar en Use instans som hanterar användning av items i inventoryt
 
        self.enemies_easy = Enemy.get_easy_enemies() #Hämtar lättare fiender från Enemy klassen
        self.enemies_hard = Enemy.get_hard_enemies() #Hämtar svårare fiender från Enemy klassen
        self.enemies_boss = Enemy.get_boss_enemies() #Hämtar boss fiender från Enemy klassen

        self.current_enemy = None

        self.direction_requirements = {"north": None, "south": None, "east": None, "west": None}

        self.setup_ui() #Anropar setup_ui metoden som skapar och arrangerar alla grafiska element i fönstret

    def setup_ui(self): #Skapar och arrangerar alla grafiska element i fönstret
        self.label = QLabel("You are a solo adventurer who has entered the py dungeon. What do you do?")
        self.label.setWordWrap(True)
        self.log = QTextEdit()  #Skapar en textedit som fungerar som en logg för spelets händelser
        self.log.setReadOnly(True)

        self.inventory_label = QLabel("Inventory:") #Skapar en label som visar att det är inventoryt som visas
        self.inventory_list = QLabel("\n".join([str(item) for item in self.inventory.get_all_items().values()])) #Skapar en label som visar alla items i inventoryt, varje item på en ny rad

        # Skapar knappar för att gå i olika riktningar
        self.btn_north = QPushButton("Go North")
        self.btn_south = QPushButton("Go South")
        self.btn_east = QPushButton("Go East")
        self.btn_west = QPushButton("Go West")

        # Ansluter knapparna till room metoden som hanterar vad som händer när spelaren försöker gå i en riktning
        self.btn_north.clicked.connect(self.room)
        self.btn_south.clicked.connect(self.room)
        self.btn_east.clicked.connect(self.room)
        self.btn_west.clicked.connect(self.room)

        self.buttons = [self.btn_north, self.btn_south, self.btn_east, self.btn_west]
        for btn in self.buttons:
            btn.setFixedWidth(200) #Sätter en fast bredd på knapparna för att de ska se bättre ut

        # Slumpa krav för varje riktning
        directions = ["north", "south", "east", "west"]
        btn_dict = {"north": self.btn_north, "south": self.btn_south, "east": self.btn_east, "west": self.btn_west}
        for direction in directions: #För varje riktning, slumpa om det krävs en nyckel för att gå dit
            room_chance = random.randint(0, 100)
            if room_chance > 50:  # 50% chans att kräva nyckel
                key_options = ["Bronze Key", "Silver Key", "Gold Key"]
                required_key = random.choice(key_options)
                self.direction_requirements[direction] = required_key
                btn_dict[direction].setText(f"Go {direction.capitalize()} ({required_key} Required)")
            else:
                self.direction_requirements[direction] = None
                btn_dict[direction].setText(f"Go {direction.capitalize()}")

        # Arrangera alla element i layouten

        inventory_layout = QVBoxLayout() #Skapar en vertikal layout för inventoryt
        inventory_layout.addWidget(self.inventory_label)
        inventory_layout.addWidget(self.inventory_list)

        button_layout = QVBoxLayout() #Skapar en vertikal layout för knapparna
        button_layout.addWidget(self.btn_north)
        button_layout.addWidget(self.btn_south)
        button_layout.addWidget(self.btn_east)
        button_layout.addWidget(self.btn_west)

        label_layout = QVBoxLayout() #Skapar en vertikal layout för label och logg
        label_layout.addWidget(self.label)
        label_layout.addWidget(self.log)

        layout = QHBoxLayout() #Skapar en horisontell layout som innehåller inventory layouten och label/button layouten
        layout.addLayout(inventory_layout)
        layout.addLayout(label_layout)
        layout.addLayout(button_layout)

        container = QWidget() #Skapar en central widget som kommer att innehålla hela layouten
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Uppdaterar inventorydisplayen
    def update_inventory_display(self):
        self.inventory_list.setText("\n".join([str(item) for item in self.inventory.get_all_items().values()]))

    # Metod för när man går in i ett rum
    def room(self):
        # Inaktivera alla riktningsknapparna
        for btn in self.buttons:
            btn.setEnabled(False)

        # Hämtar vilken knapp som klickades
        sender_btn = self.sender()
        direction = ""
        if sender_btn == self.btn_north:
            direction = "north"
        elif sender_btn == self.btn_south:
            direction = "south"
        elif sender_btn == self.btn_east:
            direction = "east"
        elif sender_btn == self.btn_west:
            direction = "west"

        # Hämta nyckelkrav för denna riktning
        required_key = self.direction_requirements[direction]

        self.log.append(f"You see a door to the {direction}. It looks like it leads to another room.")
        
        # Kontrollera om spelaren har rätt nyckel
        if required_key:
            key_item = self.inventory.get_item(required_key)
            if key_item and key_item.current > 0:
                key_item.use(1)
                self.inventory.save_to_file()
                self.update_inventory_display()
                self.log.append(f"It is locked, but you use your {required_key} to open it.")
            else:
                self.log.append(f"It is locked. You need a {required_key} to enter.")
                sender_btn.setEnabled(False)
                return

        # Slumpa beskrivning av rummet
        self.random_description = random.choice(["a dimly lit cave.", "a damp prison cell.", "a deep pit.", "a small mossy room."])
        self.log.append(f"You entered {self.random_description}.")

        QTimer.singleShot(1000, self.show_item_message)
        
        QTimer.singleShot(2500, self.check_for_enemy)

    # Bestäm om spelaren hittar ett item
    def show_item_message(self):
        self.item_chance = random.randint(0, 100)
        if self.item_chance <= 50:
            item_name = InventoryItem.slump_items()
            # Lägg till itemet i inventoryt om ett hittades
            if item_name:
                self.log.append(f"You found a {item_name}!")
                self.inventory.add_item(item_name, 1)
                self.update_inventory_display()
            else:
                self.log.append("You found nothing of value.")
        else:
            self.log.append("You found nothing of value.")

    # Bestäm om spelaren möter en fiende
    def check_for_enemy(self):
        self.enemy_chance = random.randint(0, 100)
        if self.enemy_chance <= 80:
            self.current_enemy = random.choice(self.enemies_easy)
            self.log.append(self.current_enemy.taunt())
            QTimer.singleShot(1000, self.fight_ui)
        else:
            for btn in self.buttons:
                btn.setEnabled(True)


    # Skapa UI för strid
    def fight_ui(self):
        # Avbryt om ingen fiende finns
        if not self.current_enemy:
            return
        self.label_hp = QLabel(f"Player HP: {self.player.hp} | {self.current_enemy.name} HP: {self.current_enemy.hp}")
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        # Skapa attackknapp
        self.btn_attack = QPushButton("Attack Enemy")
        self.btn_attack.clicked.connect(self.do_combat_round)

        self.inventory_label = QLabel("Inventory:") #Skapar en label som visar att det är inventoryt som visas
        self.inventory_list = QLabel("\n".join([str(item) for item in self.inventory.get_all_items().values()]))
        self.update_inventory_display()

        # Skapa knappar för att använda items i strid
        self.usable_items = [item for item in self.inventory.get_all_items().values() if item.current > 0 and item.name in ["Health Potion", "Food"]]

        self.log.append("A battle begins!")
        # Visa fiendens hot
        self.log.append(self.current_enemy.taunt())

        combat_layout = QVBoxLayout() 
        combat_layout.addWidget(self.label_hp)
        combat_layout.addWidget(self.log)
        combat_layout.addWidget(self.btn_attack)

        inventory_layout = QVBoxLayout()
        inventory_layout.addWidget(self.inventory_label)
        inventory_layout.addWidget(self.inventory_list)

        # Skapa knappar för anmckbara items
        inventory_layout.addWidget(QLabel("Usable Items:"))
        self.item_buttons = {}
        for item in self.usable_items:
            item_btn = QPushButton(f"Use {item.name} ({item.current} left)")
            item_btn.clicked.connect(lambda checked, name=item.name: self.use_item_by_name(name))
            inventory_layout.addWidget(item_btn)
            self.item_buttons[item.name] = item_btn

        main_layout = QHBoxLayout()
        main_layout.addLayout(inventory_layout)
        main_layout.addLayout(combat_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
    # Använd ett item i strid
    def use_item_by_name(self, item_name): 
        if self.use_item_handler.use_item(item_name, 1):
            if item_name == "Health Potion":
                self.log.append("You used a health potion! You feel rejuvenated! Your HP has been restored by 20 points.")
            elif item_name == "Food":
                self.log.append("You ate some food! You feel a bit better. Your HP has been restored by 10 points.")
        else:
            self.log.append(f"You don't have any {item_name}s left!")

        # Uppdatera HP-display
        if self.current_enemy:
            self.label_hp.setText(f"Player HP: {self.player.hp} | {self.current_enemy.name} HP: {self.current_enemy.hp}")
        else:
            self.label_hp.setText(f"Player HP: {self.player.hp}")

        self.update_inventory_display()
        self.update_usable_item_buttons()

        self.update_inventory_display()
        self.update_usable_item_buttons()

    def update_usable_item_buttons(self): 
        for item_name, btn in getattr(self, 'item_buttons', {}).items():
            item = self.inventory.get_item(item_name)
            if item and item.current > 0:
                btn.setText(f"Use {item.name} ({item.current} left)")
                btn.setEnabled(True)
            else:
                btn.setText(f"{item_name} (None left)")
                btn.setEnabled(False)

    # Genomför en stridsrunda
    def do_combat_round(self):
        if not self.current_enemy:
            return

        dmg = self.player.attack(self.current_enemy)
        self.log.append(f"You hit {self.current_enemy.name} for {dmg} damage!")
        if dmg == 0:
            self.log.append(f"{self.current_enemy.name} dodged your attack!")

        if self.current_enemy.is_defeated():
            self.log.append("The enemy is defeated!")
            loot = self.current_enemy.drop_loot()
            if loot:
                self.log.append(f"You found a {loot}!")
                self.inventory.add_item(loot, 1)
                self.update_inventory_display()
            self.btn_attack.setEnabled(False)

            self.current_enemy.reset_hp()

            self.current_enemy = None
            QTimer.singleShot(2000, self.setup_ui)
            return
        

        dmg_enemy = self.current_enemy.attack(self.player)
        self.log.append(f"{self.current_enemy.name} hits you for {dmg_enemy} damage!")
        if dmg_enemy == 0:
            self.log.append(f"You dodged {self.current_enemy.name}'s attack!")

        if not self.player.is_alive():
            self.log.append("You have been defeated! Game Over.")
            self.btn_attack.setEnabled(False)
            self.btn_use_item.setEnabled(False)

            self.current_enemy.reset_hp()
            self.current_enemy = None

        self.label_hp.setText(f"Player HP: {self.player.hp} | {self.current_enemy.name} HP: {self.current_enemy.hp}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RPGWindow()
    window.show()
    sys.exit(app.exec())