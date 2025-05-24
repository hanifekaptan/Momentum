from crudSettings import SettingsManager
from crudTask import TaskManager
from crudPomodoro import PomodoroManager

settingsManager = SettingsManager()
taskManager = TaskManager()
pomodoroManager = PomodoroManager()

settingsManager.create_fake_data()
taskManager.create_fake_data()
pomodoroManager.create_fake_data()