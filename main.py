import sys
import os

projectRoot = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, projectRoot)

from PyQt5.QtWidgets import QApplication
from src.core.welcome import Welcome
from src.core.tasks import Tasks
from src.core.calendar import Calendar
from src.core.pomodoro import Pomodoro
from src.core.profile import Profile


if __name__ == "__main__":

    app = QApplication(sys.argv)

    welcome = Welcome()
    tasks = Tasks()
    calendar = Calendar()
    pomodoro = Pomodoro()
    profile = Profile()

    allWindows = [
        welcome,
        tasks,
        calendar,
        pomodoro,
        profile
    ]

    def showWindow(windowToShow):
        for window in allWindows:
            if window is not windowToShow and window.isVisible():
                # açık olan pencere açılmak istenen pencere ile aynı değilse açık pencereyi kapat.
                window.close()
        if not window.isVisible():
            # eğer açık pencere yoksa (yani açılmak istenen pencere açık
            # pencereden farklı bir değere sahip ise) açılmak istenen pencereyi aç
            windowToShow.show()

    for window in allWindows:
        window.ui.welcomeButton.clicked.connect(lambda: showWindow(welcome))
        window.ui.tasksButton.clicked.connect(lambda: showWindow(tasks))
        window.ui.calendarButton.clicked.connect(lambda: showWindow(calendar))
        window.ui.pomodoroButton.clicked.connect(lambda: showWindow(pomodoro))
        window.ui.profileButton.clicked.connect(lambda: showWindow(profile))

    showWindow(welcome)
    sys.exit(app.exec_())
