from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from src.ui.generated.tasks import Ui_MainWindow
from src.core.editTasks import EditTasks
from src.core.databaseManagement.crudTask import TaskManager
from datetime import datetime
import sys
import os

class Tasks(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setQSS()
        self.dbm = TaskManager()

        self.currentStateIndex = 0
        self.num_states = 2
        self.ui.sort.clicked.connect(self.callSortTasks)
        self.ui.enterNewTask.returnPressed.connect(self.createNewTask)

        self.uploadTask()
        
    def setQSS(self):
        qssFile = os.path.join("src", "styles", "tasks.qss")
        try:
            with open(qssFile, "r", encoding="utf-8") as f:
                qss = f.read()
                self.setStyleSheet(qss)
        except FileNotFoundError:
            print(f"Warning: QSS not found at {qssFile}", file = sys.stderr)
        except Exception as e:
            print(f"Error loading QSS {qssFile}: {e}", file = sys.stderr)

    def getCheckboxAtRuntime(self):
        checkboxList = self.ui.scrollAreaWidgetContents.findChildren(QtWidgets.QCheckBox)
        return checkboxList
     
    def countOfTasksAtRuntime(self):
        checkboxList = self.getCheckboxAtRuntime()
        count = len(checkboxList)
        return count
    
    def deleteCheckbox(self):
        checkboxList = self.getCheckboxAtRuntime()
        for checkbox in checkboxList:
            self.ui.gridLayout.removeWidget(checkbox)
            checkbox.deleteLater()

    def removeSpacerItem(self):
        self.ui.gridLayout.removeItem(self.ui.spacerItem3)
        self.ui.gridLayout.update()

    def addSpacerItem(self):
        self.ui.spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.ui.gridLayout.addItem(self.ui.spacerItem3, self.countOfTasksAtRuntime() + 2, 0, 1, 3)
        self.ui.gridLayout.update()

    def getData(self, criteria):
        data = self.dbm.get_all_tasks_sorted_custom(criteria)
        return data
    
    def uploadTask(self, criteria = [("is_completed", "ASC"), ("priority", "DESC")]):
        self.deleteCheckbox()
        allTasks = self.getData(criteria)
        self.removeSpacerItem()
        for task in allTasks:
            countOfTasks = self.countOfTasksAtRuntime()
            objectName = task["task_id"]
            title = task["title"]
            completed = task["is_completed"]
            self.createTask(countOfTasks, objectName, title, bool(completed))
        self.addSpacerItem()

    def getDataFromUI(self):
        newTask = self.ui.enterNewTask.text()
        if newTask == "":
            self.noneTaskError()
            return None
        self.ui.enterNewTask.clear()
        data = {
            "title": newTask,
            "is_completed": False
        }
        return data

    def createNewTask(self):
        data = self.getDataFromUI()
        startDate = datetime(1, 1, 1).strftime("%Y-%m-%d")
        endDate = datetime(1, 1, 1).strftime("%Y-%m-%d")
        tag = None
        priority = 0
        if data is not None:
            self.dbm.insert_task(title=data["title"],
                                 is_completed=data["is_completed"],
                                 start_date=startDate,
                                 end_date=endDate,
                                 priority=priority,
                                 tag=tag)
            self.uploadTask()
    
    def createTask(self, countOfTasks, taskId, title, taskCompleted):
        """adds a new task into the task list."""
        objectName = ("task"+str(taskId))
        self.sampleTask = QtWidgets.QCheckBox(self.ui.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sampleTask.sizePolicy().hasHeightForWidth())
        self.sampleTask.setSizePolicy(sizePolicy)
        self.sampleTask.setMinimumSize(QtCore.QSize(50, 50))
        self.sampleTask.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Golos Text Medium")
        font.setBold(False)
        font.setWeight(50)
        self.sampleTask.setFont(font)
        self.sampleTask.setStyleSheet("")
        self.sampleTask.setObjectName(objectName)
        self.ui.gridLayout.addWidget(self.sampleTask, countOfTasks + 1, 0, 1, 3)
        self.sampleTask.setText(title)
        self.sampleTask.setChecked(taskCompleted)
        self.sampleTask.installEventFilter(self)
        self.sampleTask.stateChanged.connect(self.updateTaskCompletion)

    def sortTasks(self, orderBy, orderType):
        criteria = [("is_completed", "ASC"), (orderBy, orderType)]
        self.uploadTask(criteria)
        
    def callSortTasks(self):
        self.currentStateIndex = (self.currentStateIndex + 1) % self.num_states
        if self.currentStateIndex == 0:
            self.sortTasks("priority", "DESC")
        elif self.currentStateIndex == 1:
            self.sortTasks("title", "ASC")

    def updateTaskCompletion(self):
        objectName = self.sender().objectName()
        taskId = int(str(objectName).lstrip("task"))
        taskCompletion = self.sender().isChecked()
        self.dbm.update_task(taskId, is_completed=taskCompletion)
        self.uploadTask()

    def eventFilter(self, checkBoxObject, event):
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            if event.button() == QtCore.Qt.LeftButton:
                self.openEditTasksDialog(checkBoxObject)
                return True
        return super().eventFilter(checkBoxObject, event)

    def openEditTasksDialog(self, senderItem):
        editTasksDialog = EditTasks(senderItem)
        editTasksDialog.exec_()
        self.uploadTask()

    def noneTaskError(self):
        errorMessage = QtWidgets.QMessageBox()
        errorMessage.setWindowTitle("Error")
        errorMessage.setText("Please enter a task description.")
        errorMessage.setIcon(QtWidgets.QMessageBox.Warning)
        errorMessage.exec_()
        return None
