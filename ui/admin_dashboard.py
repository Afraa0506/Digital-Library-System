# ui/admin_dashboard.py
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton)
from PyQt6.QtGui import QIcon
from backend.database import Database


class AdminDashboard(QWidget):
    def __init__(self, logout_callback):
        super().__init__()
        self.db = Database("data/library.db")
        self.logout_callback = logout_callback
        self.setWindowTitle("Admin Dashboard")
        self.setWindowIcon(QIcon("ui/assets/admin_icon.svg"))
        self.setFixedSize(600, 400)

        self.init_ui()
        self.load_usage_logs()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("📊 Usage Logs")
        title.setStyleSheet("font-size:16px; font-weight:bold; margin:10px;")
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["User ID", "Resource ID", "Status", "Log ID"])
        layout.addWidget(self.table)

        # NEW: Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("background:#f44336; color:white; padding:5px; border-radius:6px;")
        logout_btn.clicked.connect(self.logout_callback)
        layout.addWidget(logout_btn)

        self.setLayout(layout)

    def load_usage_logs(self):
        rows = self.db.get_usage_logs()   # updated to use helper
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
