from PyQt5.QtWidgets import QMainWindow
from src.ui.generated.welcome import Ui_MainWindow
import sys
import os

class Welcome(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setQSS()

        self.ui.goCalendarButton.clicked.connect(self.clickCalendarButton)
        self.ui.goTasksButton.clicked.connect(self.clickTasksButton)
        self.ui.goPomodoroButton.clicked.connect(self.clickPomodoroButton)
        self.ui.goProfileButton.clicked.connect(self.clickProfileButton)
   
    def setQSS(self):
        qssFile = os.path.join("src", "styles", "welcome.qss")
        try:
            with open(qssFile, "r", encoding="utf-8") as f:
                qss = f.read()
                self.setStyleSheet(qss)
        except FileNotFoundError:
            print(f"Warning: QSS not found at {qssFile}", file = sys.stderr)
        except Exception as e:
            print(f"Error loading QSS {qssFile}: {e}", file = sys.stderr)

    def clickCalendarButton(self):
        self.ui.calendarButton.click()

    def clickTasksButton(self):
        self.ui.tasksButton.click()

    def clickPomodoroButton(self):
        self.ui.pomodoroButton.click()

    def clickProfileButton(self):
        self.ui.profileButton.click()
