import sys
from PyQt6.QtWidgets import QApplication

from ui.login_window import LoginWindow
from ui.student_dashboard import StudentDashboard
from ui.teacher_dashboard import TeacherDashboard
from ui.admin_dashboard import AdminDashboard


class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = None
        self.show_login()

    def show_login(self):
        """Start with the login window"""
        self.window = LoginWindow(self.switch_to_dashboard)
        self.window.show()
        sys.exit(self.app.exec())

    def switch_to_dashboard(self, role, user_id):
        """Switch to correct dashboard after login"""
        self.window.close()

        if role == "student":
            self.window = StudentDashboard(user_id, self.switch_to_login)
        elif role == "teacher":
            self.window = TeacherDashboard(user_id, self.switch_to_login)
        elif role == "admin":
            self.window = AdminDashboard(self.switch_to_login)
        else:
            print("Unknown role, defaulting to student.")
            self.window = StudentDashboard(user_id, self.switch_to_login)

        self.window.show()

    def switch_to_login(self):
        """Logout: return to login window"""
        self.window.close()
        self.window = LoginWindow(self.switch_to_dashboard)
        self.window.show()


if __name__ == "__main__":
    AppController()
