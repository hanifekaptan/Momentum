from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QColor, QBrush, QTextCharFormat, QFont
from PyQt5.QtCore import Qt, QDate
from PyQt5 import QtWidgets, QtCore
from src.ui.generated.calender import Ui_MainWindow
from src.core.databaseManagement.crudTask import TaskManager
import sys
import os

class Calendar(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.dbm = TaskManager()
        self.setQSS()

        self.ui.calendarWidget.selectionChanged.connect(self.updateActivityList)

    def setQSS(self):
        qssFile = os.path.join("src", "styles", "calendar.qss")
        try:
            with open(qssFile, "r", encoding="utf-8") as f:
                qss = f.read()
                self.setStyleSheet(qss)
                self.enhanceCalendarStyles()
        except FileNotFoundError:
            print(f"Warning: QSS not found at {qssFile}", file = sys.stderr)
        except Exception as e:
            print(f"Error loading QSS {qssFile}: {e}", file = sys.stderr)

    def formatWeekday(self):
        # haftanın günleri arka plan rengi
        qcolor = QColor()
        weekdayFormat = QTextCharFormat()
        qcolor.setNamedColor("#00373737")
        weekdayFormat.setBackground(QBrush(qcolor, Qt.SolidPattern))
        self.ui.calendarWidget.setHeaderTextFormat(weekdayFormat)
        
    def formatWeekend(self):
        # hafta sonu metin rengi
        qcolor = QColor()
        weekendFormat = QTextCharFormat()
        qcolor.setNamedColor("#c6e5ad")
        weekendFormat.setForeground(QBrush(qcolor, Qt.SolidPattern))
        self.ui.calendarWidget.setWeekdayTextFormat(Qt.Saturday, weekendFormat)
        self.ui.calendarWidget.setWeekdayTextFormat(Qt.Sunday, weekendFormat)
        
    def formatToday(self):
        # bugün metin rengi
        qcolor = QColor()
        todayFormat = QTextCharFormat()
        today = QDate.currentDate()
        qcolor.setNamedColor("#c6e5ad")
        todayFormat.setForeground(QBrush(qcolor, Qt.SolidPattern))
        todayFormat.setFont(QFont("Times New Roman", 25, QFont.Bold))
        todayFormat.setFontUnderline(True)
        self.ui.calendarWidget.setDateTextFormat(today, todayFormat)

    def formatSpecialDays(self, qcolor: QColor, date: QDate):
        # özel günlerin işaretlenmesi
        specialDaysFormat = QTextCharFormat()
        specialDaysFormat.setBackground(QBrush(qcolor, Qt.SolidPattern))
        specialDaysFormat.setFont(QFont("Times New Roman", 20, QFont.Bold))
        self.ui.calendarWidget.setDateTextFormat(date, specialDaysFormat)

    def enhanceCalendarStyles(self):
        self.formatWeekday()
        self.formatWeekend()
        self.formatToday()
        self.applyFormatSpecialDays()

    def getSpecialDayData(self):
        uncompletedTasks = self.dbm.get_all_task_completion(False)
        specialDays = []
        for task in uncompletedTasks:
            data = {
                "task_id": task["task_id"],
                "title": task["title"],
                "start_date": task["start_date"],
                "end_date": task["end_date"],
                "priority": task["priority"]
            }
            specialDays.append(data)
        return specialDays
    
    def getColorByPriority(self, priority: int):
        qcolor = QColor()
        if priority in range(8, 11):
            qcolor.setNamedColor("#b74005")
        elif priority in range(6, 8):
            qcolor.setNamedColor("#ddc151")
        elif priority in range(0, 6) or priority is None:
            qcolor.setNamedColor("#6e9655")
        return qcolor

    def convertDateFormat(self, date, toFormat : str | QDate = "str"):
        if toFormat == "str":
            return date.toString("yyyy-MM-dd")
        elif toFormat == "qdate":
            return QDate.fromString(date, "yyyy-MM-dd")

    def applyFormatSpecialDays(self):
        dataList = self.getSpecialDayData()
        for data in dataList:
            qdate = self.convertDateFormat(data["start_date"], "qdate")
            qcolor = self.getColorByPriority(data["priority"])
            self.formatSpecialDays(qcolor, qdate)
    
    def countOfActivityInOneDay(self, date: str):
        # count = 0
        # for data in self.getSpecialDayData():
        #     if data["start_date"] == date:
        #         count += 1
        count = len(self.dbm.get_task_in_one_day(date))
        return count
    
    def updateActivityList(self):
        date = self.ui.calendarWidget.selectedDate()
        self.displayActivity(date)
    
    def addDescriptionTitle(self):
        self.description = QtWidgets.QLabel(self.ui.descriptionFrame)
        self.description.setMaximumSize(400, 20)
        self.description.setMinimumSize(300, 20)
        self.description.setAlignment(QtCore.Qt.AlignCenter)
        self.description.setObjectName("description")
        self.description.setText("Activities\n")
        self.ui.verticalLayout_3.addWidget(self.description)

    def deleteLabels(self):
        labelList = self.ui.descriptionFrame.findChildren(QtWidgets.QLabel)
        for label in labelList:
            self.ui.verticalLayout_3.removeWidget(label)
            label.deleteLater()

    def removeSpacer(self):
        self.ui.verticalLayout_3.removeItem(self.ui.spacerItem2)
        self.ui.verticalLayout_3.update()

    def addSpacer(self):
        self.ui.spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.ui.verticalLayout_3.addItem(self.ui.spacerItem2)
        self.ui.verticalLayout_3.update()

    def createActivityDescription(self, count, description: str):
        self.description = QtWidgets.QLabel(self.ui.descriptionFrame)        
        self.description.setWordWrap(True)
        self.description.setText(f"{count}. {description}\n")
        self.description.setAlignment(QtCore.Qt.AlignLeft)
        self.ui.verticalLayout_3.addWidget(self.description)

    def displayActivity(self, date: QDate):
        self.deleteLabels()
        self.addDescriptionTitle()
        self.removeSpacer()
        date = self.convertDateFormat(date, "str")
        data = self.dbm.get_task_in_one_day(date)
        for i, d in enumerate(data):
            self.createActivityDescription(i+1, d["title"])
        self.addSpacer()
        


