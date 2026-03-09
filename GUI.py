import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QWidget, QTextEdit
from engine import Character # Importing your logic!

class RPGWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Py Dungeon")
        
        # Initialize Game Data
        self.player = Character("Hero", 100, 10)
        self.enemy = Character("Slime", 30, 5)

        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        self.label_hp = QLabel(f"Player HP: {self.player.hp} | Enemy HP: {self.enemy.hp}")
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
        # Player attacks enemy
        dmg = self.player.attack(self.enemy)
        self.log.append(f"You hit {self.enemy.name} for {dmg} damage!")
        
        if not self.enemy.is_alive():
            self.log.append("The enemy is defeated!")
            self.btn_attack.setEnabled(False)
        
        # Update HP display
        self.label_hp.setText(f"Player HP: {self.player.hp} | Enemy HP: {self.enemy.hp}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RPGWindow()
    window.show()
    sys.exit(app.exec())
