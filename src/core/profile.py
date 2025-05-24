from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QPixmap, QImage
from src.ui.generated.profile import Ui_MainWindow
from src.core.databaseManagement.crudPomodoro import PomodoroManager
from src.core.databaseManagement.crudSettings import SettingsManager
from src.core.databaseManagement.crudTask import TaskManager
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
import numpy as np
import sys
import os


class Profile(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.dbmPomodoro = PomodoroManager()
        self.dbmSettings = SettingsManager()
        self.dbmTasks = TaskManager()
        self.setQSS()

        self.loadSettings()
        self.setPomodoroGraphsToLabels()
        self.setTaskGraphToLabel()

        self.ui.saveChangesButton.clicked.connect(self.saveChanges)

    def setQSS(self):
        """Loads the "profile.qss" file and sets it to window."""
        qssFile = os.path.join("src", "styles", "profile.qss")
        try:
            with open(qssFile, "r", encoding="utf-8") as f:
                qss = f.read()
                self.setStyleSheet(qss)
        except FileNotFoundError:
            print(f"Warning: QSS not found at {qssFile}", file = sys.stderr)
        except Exception as e:
            print(f"Error loading QSS {qssFile}: {e}", file = sys.stderr)

    def getSettingsData(self):
        data = self.dbmSettings.get_user_data()
        return data

    def loadSettings(self):
        data = self.getSettingsData()
        self.ui.userNameInput.setText(data["user_name"])
        self.ui.emailInput.setText(data["email"])
        self.ui.genderInput.setCurrentText(data["gender"])
        self.ui.birthDateInput.setDate(self.dateFormat(data["birth_date"], "qdate"))

    def dateFormat(self, date, toFormat = "str"):
        if toFormat == "str":
            return date.toString("yyyy-MM-dd")
        elif toFormat == "qdate":
            return QDate.fromString(date, "yyyy-MM-dd")

    def saveChanges(self):
        data = {
            "user_name": self.ui.userNameInput.text(),
            "email": self.ui.emailInput.text(),
            "gender": self.ui.genderInput.currentText(),
            "birth_date": self.dateFormat(self.ui.birthDateInput.date(), "str")
        }
        self.dbmSettings.update_user_data(data["user_name"], data["email"], data["birth_date"], data["gender"])
        self.loadSettings()
        return data
    
    def getPomodoroData(self):
        # pomodoro counter, total study time, total break time bilgilerini içerir
        data = self.dbmPomodoro.get_pomodoro_summary_data()
        return data
    
    def getTaskData(self):
        data = self.dbmTasks.get_task_summary_data()
        return data
    
    def loadPomodoroData(self):
        data = self.getPomodoroData()
        count = data[0]["count"] + data[1]["count"]
        for d in data:
            self.ui.PomodoroCounterOutput.setText(str(count))
            if d["pomodoro_type"] == "study":
                totalStudyTime = d["total"]
                self.ui.totalStudyTimeOutput.setText(str(totalStudyTime))
            elif d["pomodoro_type"] == "break":
                totalBreakTime = d["total"]
                self.ui.totalBreakTimeOutput.setText(str(totalBreakTime))

    def setPomodoroGraphsToLabels(self):
        self.loadPomodoroData()
        data = self.getPomodoroData()
        fig = self.createPieChart(data, "pomodoro",
                                  figsize=(4, 4),
                                  color = ["#a9c394", "#ffdf5d"],
                                  ha = "center", va = "top",
                                  set_y0 = 1, set_y1 = 0.9)
        pixmap = self.figToPixmap(fig)
        self.ui.pomodoroGraph.setPixmap(pixmap)
        plt.close(fig)

    def setTaskGraphToLabel(self):
        data = self.getTaskData()
        fig = self.createPieChart(data, "task",
                                  figsize=(4, 4),
                                  color = ["#e49595", "#aeafec"], # "#dd8800"],
                                  ha = "center", va = "top",
                                  set_y0 = 0.9, set_y1 = 0.9)
        pixmap = self.figToPixmap(fig)
        self.ui.taskGraph.setPixmap(pixmap)
        plt.close(fig)

    def getLabel(self, data, title):
        if title == "pomodoro":
            labels = ["Break", "Study"]
            values = [data[0]["total"], data[1]["total"]]
        elif title == "task":
            labels = ["Completed", "Uncompleted"]
            values = [data[1]["count"], data[0]["count"]]
        return labels, values

    def createPieChart(self, data, title="pomodoro",
                       figsize = (4, 4),
                       color = ['#b74005', '#6e9655'],
                       ha = "center", va = "center",
                       set_y0 = 1.0, set_y1 = -1.2):
        labels, values = self.getLabel(data, title)
        fig, ax = plt.subplots(figsize=figsize, facecolor="#1c1c1c")
        wedges, texts, autotexts = ax.pie(
            values, 
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=color,
            explode=(0, 0.1),
            pctdistance=0.5,
            labeldistance=1.1,
            textprops={
                'ha': ha, 
                'va': va,
                'color': 'white'
            }
            )
        texts[0].set_y(set_y0)
        texts[1].set_y(set_y1) 
        ax.axis('equal')
        ax.set_title(f"{title.capitalize()} Summary Graph", pad=20, color="#e8e9e0")
        fig.tight_layout()
        return fig

    def figToPixmap(self, fig):
        """Matplotlib figürünü QPixmap'e dönüştür"""
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        width, height = fig.get_size_inches() * fig.get_dpi()  # numpy.float64 döner
        width, height = int(width), int(height)
        image = np.frombuffer(canvas.tostring_rgb(), dtype='uint8').reshape(height, width, 3)

        # QImage oluştururken bytes_per_line ekleyin (RGB olduğu için 3 * width)
        bytes_per_line = 3 * width
        qimage = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # QPixmap'e dönüştür ve döndür
        return QPixmap.fromImage(qimage)
    