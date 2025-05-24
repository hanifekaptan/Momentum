from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
from src.ui.generated.pomodoro import Ui_MainWindow
from src.core.editStudy import EditStudy
from src.core.databaseManagement.crudPomodoro import PomodoroManager
import sys
import os


class Pomodoro(QMainWindow, Ui_MainWindow):
    workMinutes = 45
    breakMinutes = 15

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.settingsDialog = EditStudy()
        self.dbm = PomodoroManager()
        self.ui.setupUi(self)
        self.setQSS()

        self.activeSession = "work"
        self.sessionIsActive = False
        self.lastSessionDuration = 0
        self.pomodoroDuration = self.workMinutes * 60
        self.timeRemaining = self.pomodoroDuration
        self.ui.timeSlider.setRange(0, self.pomodoroDuration)
        self.ui.timeSlider.setValue(0)

        self.initTimer()
        self.loadPomodoroConfig()
        self.updateActiveSessionDisplay()
        self.updatePrevNextDisplay()

        self.ui.editButton.clicked.connect(self.openSettingsDialog)
        self.ui.playButton.clicked.connect(self.playSession)
        self.ui.stopButton.clicked.connect(self.stopSession)
        self.ui.stopButton.setEnabled(False)

    def setQSS(self):
        """Loads the "pomodoro.qss" file and sets it to window."""
        qssFile = os.path.join("src", "styles", "pomodoro.qss")
        try:
            with open(qssFile, "r", encoding="utf-8") as f:
                qss = f.read()
                self.setStyleSheet(qss)
        except FileNotFoundError:
            print(f"Warning: QSS not found at {qssFile}", file = sys.stderr)
        except Exception as e:
            print(f"Error loading QSS {qssFile}: {e}", file = sys.stderr)

    def initTimer(self):
        self.timer = QTimer(self)
        self.timer.setInterval(1000) # 1000 milisaniye = 1 saniye aralıkla çalış
        self.timer.timeout.connect(self.updateTimer)
    
    def setPomodoroDuration(self):
        if self.activeSession == "work":
            self.pomodoroDuration = self.workMinutes * 60
        elif self.activeSession == "break":
            self.pomodoroDuration = self.breakMinutes * 60

    def changedWorkBreakMinutes(self, workMinutes, breakMinutes):
        self.workMinutes = workMinutes
        self.breakMinutes = breakMinutes

    def loadPomodoroConfig(self):
        self.settingsDialog.dataSent.connect(self.changedWorkBreakMinutes)
        self.setPomodoroDuration()
        self.timeRemaining = self.pomodoroDuration
        self.ui.timeSlider.setRange(0, self.pomodoroDuration)
        self.ui.timeSlider.setValue(self.pomodoroDuration - self.timeRemaining)
        self.updateActiveSessionDisplay()
        self.updatePrevNextDisplay()

    def openSettingsDialog(self):
        self.stopSession()
        self.settingsDialog.exec_()
        self.loadPomodoroConfig()

    def formatTime(self, seconds):
        if seconds is None or seconds < 0:
            return "00:00:00"
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02}:{minutes:02}:{secs:02}"

    def playSession(self):
        if not self.sessionIsActive:
            self.sessionIsActive = True
            if self.timeRemaining <= 0:
                self.startNextSession()
            self.timer.start()
            self.ui.playButton.setEnabled(False)
            self.ui.stopButton.setEnabled(True)
            self.updateActiveSessionDisplay()
            self.updatePrevNextDisplay()

    def stopSession(self):
        if self.sessionIsActive:
            self.sessionIsActive = False
            self.timer.stop()
            self.ui.playButton.setEnabled(True)
            self.ui.stopButton.setEnabled(False)

    def updateTimer(self):
        self.timeRemaining -= 1
        if self.timeRemaining <= 0:
            self.sessionCompleted() # Süre bittiğinde tamamlanma metodunu çağır
        else:
            self.updateActiveSessionDisplay() # Süre bitmediyse ekranı güncelle

    def updateActiveSessionDisplay(self):
        tempTime = self.formatTime(self.timeRemaining)
        self.ui.presentTime.setText(tempTime)
        self.ui.timeSlider.setValue(self.pomodoroDuration - self.timeRemaining)
    
    def getNextSessionDuration(self):
        if self.activeSession == "work":
            return self.breakMinutes * 60
        elif self.activeSession == "break":
            return self.workMinutes * 60
        
    def updatePrevNextDisplay(self):
        prevTime = self.formatTime(self.lastSessionDuration)
        self.ui.previousTime.setText(prevTime)
        nextTime = self.getNextSessionDuration()
        nextTime = self.formatTime(nextTime)
        self.ui.nextTime.setText(nextTime)

    def sessionCompleted(self):
        self.timer.stop()
        self.sessionIsActive = False
        self.dbm.insert_pomodoro_log(self.pomodoroDuration, self.activeSession)
        self.lastSessionDuration = self.pomodoroDuration
        self.timeRemaining = 0
        self.startNextSession()
        self.updateActiveSessionDisplay()
        self.updatePrevNextDisplay()
        self.ui.playButton.setEnabled(True)
        self.ui.stopButton.setEnabled(False)

    def startNextSession(self):
        self.pomodoroDuration = self.getNextSessionDuration()
        self.timeRemaining = self.pomodoroDuration
        self.activeSession = "work" if self.activeSession == "break" else "break"
        self.playSession()
        