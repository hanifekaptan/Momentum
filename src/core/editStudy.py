from PyQt5.QtWidgets import QDialog
from src.ui.generated.editStudy import Ui_Dialog
from PyQt5.QtCore import pyqtSignal, QObject
import sys
import os


class EditStudy(QDialog, Ui_Dialog):
    dataSent = pyqtSignal(int, int)

    def __init__(self, parent=None): # Dialogs often take a parent
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setQSS()

        self.ui.saveButton.clicked.connect(self.saveChanges)
        self.ui.cancelButton.clicked.connect(self.quitDialog)

    def setQSS(self):
        """Loads the "editStudy.qss" file and sets it to window."""
        qssFile = os.path.join("src", "styles", "editStudy.qss")
        try:
            with open(qssFile, "r", encoding="utf-8") as f:
                qss = f.read()
                self.setStyleSheet(qss)
        except FileNotFoundError:
            print(f"Warning: QSS not found at {qssFile}", file = sys.stderr)
        except Exception as e:
            print(f"Error loading QSS {qssFile}: {e}", file = sys.stderr)
        
    def saveChanges(self):
        studyTime = self.formatTime(self.ui.studyTime.time())
        restTime = self.formatTime(self.ui.restTime.time())
        self.dataSent.emit(studyTime, restTime)
        self.close()

    def formatTime(self, time):
        return time.hour() * 60 + time.minute()
    
    def quitDialog(self):
        self.ui.close()