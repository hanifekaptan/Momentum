from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QDate
from src.ui.generated.editTasks import Ui_Dialog
from src.core.databaseManagement.crudTask import TaskManager
from datetime import datetime
import sys
import os

class EditTasks(QDialog, Ui_Dialog):
    def __init__(self, senderItem):
        super().__init__(senderItem)
        self.ui = Ui_Dialog()
        self.dbm = TaskManager()
        self.senderItem = senderItem
        self.ui.setupUi(self)
        self.setQSS()
        self.loadTask()
        self.ui.saveButton.clicked.connect(self.saveTask)
        self.ui.cancelButton.clicked.connect(self.quitDialog)
        self.ui.deleteButton.clicked.connect(self.deleteTask)

    def setQSS(self):
        """Loads the "editTasks.qss" file and sets it to window."""
        qssFile = os.path.join("src", "styles", "editTasks.qss")
        try:
            with open(qssFile, "r", encoding="utf-8") as f:
                qss = f.read()
                self.setStyleSheet(qss)
                print(f"Successfully loaded style from: {qssFile}")
        except FileNotFoundError:
            print(f"Warning: QSS not found at {qssFile}", file = sys.stderr)
        except Exception as e:
            print(f"Error loading QSS {qssFile}: {e}", file = sys.stderr)

    def getData(self):
        taskId = int(self.senderItem.objectName().lstrip("task"))
        task = self.dbm.get_task(taskId)
        nullDate = datetime(25, 1, 1)
        startDate = self.format_date(task["start_date"]) if task["start_date"] is not None else nullDate
        endDate = self.format_date(task["end_date"]) if task["end_date"] is not None else nullDate
        tag = task["tag"] if task["tag"] is not None else None
        priority = task["priority"] if task["priority"] is not None else 0
        data = {
            "task_id": taskId,
            "title": task["title"],
            "tag": tag,
            "start_date": startDate,
            "end_date": endDate,
            "priority": priority
        }
        return data


    def loadTask(self):
        """Loads the task information from the database."""
        task = self.getData()
        self.ui.task.setText(task["title"])
        self.ui.tag.setText(task["tag"])
        self.ui.startDate.setDateTime(task["start_date"])
        self.ui.endDate.setDateTime(task["end_date"])
        self.ui.priority.setValue(task["priority"])
        
    def saveTask(self):
        """Saves the task information to the database."""
        taskId = int(self.senderItem.objectName().lstrip("task"))
        title = self.ui.task.text()
        tag = self.ui.tag.text()
        startDate = self.ui.startDate.date().toString("yyyy-MM-dd")
        endDate = self.ui.endDate.date().toString("yyyy-MM-dd")
        priority = (self.ui.priority.value()) // 10
        print(title, tag, startDate, endDate, priority)
        self.dbm.update_task(task_id=taskId,
                            title=title,
                            tag=tag,
                            start_date=startDate,
                            end_date=endDate,
                            priority=priority)

    def deleteTask(self):
        """Deletes the task from the database."""
        taskId = int(self.senderItem.objectName().lstrip("task"))
        self.dbm.delete_task(taskId)
        self.quitDialog()

    def clearData(self):
        """Clears the data from the ui."""
        nullDate = datetime(1, 1, 1)
        self.ui.task.clear()
        self.ui.tag.clear()
        self.ui.startDate.setDateTime(nullDate)
        self.ui.endDate.setDateTime(nullDate)
        self.ui.priority.setValue(50)

    def quitDialog(self):
        """Quits the edit tasks window."""
        self.clearData()
        self.close()

    def format_date(self, datetime_str):
        datetime_format = "%Y-%m-%d"
        try:
            return datetime.strptime(datetime_str, datetime_format)
        except ValueError:
            return datetime.strptime(datetime_str, datetime_format)