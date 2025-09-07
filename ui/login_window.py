from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout, QMessageBox)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from backend.database import Database


class LoginWindow(QWidget):
    def __init__(self, switch_to_dashboard):
        super().__init__()
        self.db = Database("data/library.db")
        self.switch_to_dashboard = switch_to_dashboard
        self.setWindowTitle("Digital Library - Login")
        self.setWindowIcon(QIcon("ui/assets/book_icon.svg"))
        self.setFixedSize(400, 350)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("📚 Digital Library Login")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)

        # Email input
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email")
        layout.addWidget(self.email_input)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Role input
        self.role_input = QLineEdit()
        self.role_input.setPlaceholderText("Role (student / teacher / admin)")
        layout.addWidget(self.role_input)

        # Buttons
        btn_layout = QHBoxLayout()
        login_btn = QPushButton("Login")
        login_btn.setStyleSheet("background:#4CAF50; color:white; padding:5px; border-radius:6px;")
        login_btn.clicked.connect(self.login)

        signup_btn = QPushButton("Signup")
        signup_btn.setStyleSheet("background:#2196F3; color:white; padding:5px; border-radius:6px;")
        signup_btn.clicked.connect(self.signup)

        btn_layout.addWidget(login_btn)
        btn_layout.addWidget(signup_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_input.text().strip().lower()

        cur = self.db.conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=? AND password=? AND role=?", (email, password, role))
        user = cur.fetchone()

        print("DEBUG login:", email, role, "->", user)  # 🔎 Debugging line

        if user:
            QMessageBox.information(self, "Success", f"Welcome back, {user[1]}!")
            self.switch_to_dashboard(role, user[0])  # user_id
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials.")

    def signup(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_input.text().strip().lower()

        if not email or not password or not role:
            QMessageBox.warning(self, "Error", "Fill all fields.")
            return

        cur = self.db.conn.cursor()
        try:
            cur.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                        (email.split("@")[0], email, password, role))
            self.db.conn.commit()
            QMessageBox.information(self, "Success", f"Signup successful for {email} as {role}. Please login.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Signup failed: {e}")
