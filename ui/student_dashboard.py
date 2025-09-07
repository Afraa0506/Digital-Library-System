# ui/student_dashboard.py
from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QTableWidget,
                             QTableWidgetItem, QMessageBox)
from PyQt6.QtGui import QIcon
from backend.database import Database
import os
import shutil
from pathlib import Path


class StudentDashboard(QWidget):
    def __init__(self, user_id, logout_callback):
        super().__init__()
        self.db = Database("data/library.db")
        self.user_id = user_id
        self.logout_callback = logout_callback
        self.setWindowTitle("Student Dashboard")
        self.setWindowIcon(QIcon("ui/assets/student_icon.svg"))
        self.setFixedSize(600, 400)

        self.init_ui()
        self.load_resources()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("📖 Available Resources")
        title.setStyleSheet("font-size:16px; font-weight:bold; margin:10px;")
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Title", "Type", "Author"])
        layout.addWidget(self.table)

        borrow_btn = QPushButton("Borrow Selected")
        borrow_btn.setStyleSheet("background:#FF9800; color:white; padding:5px; border-radius:6px;")
        borrow_btn.clicked.connect(self.borrow_selected)
        layout.addWidget(borrow_btn)

        # NEW: Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("background:#f44336; color:white; padding:5px; border-radius:6px;")
        logout_btn.clicked.connect(self.logout_callback)
        layout.addWidget(logout_btn)

        self.setLayout(layout)

    def load_resources(self):
        cur = self.db.conn.cursor()
        cur.execute("SELECT resource_id, title, type, author FROM resources")
        rows = cur.fetchall()
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(row[1]))
            self.table.setItem(i, 1, QTableWidgetItem(row[2]))
            self.table.setItem(i, 2, QTableWidgetItem(row[3]))

    def borrow_selected(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "Select a resource first.")
            return
        cur = self.db.conn.cursor()
        cur.execute("SELECT resource_id FROM resources LIMIT 1 OFFSET ?", (selected_row,))
        resource = cur.fetchone()
        if resource:
            self.db.borrow_resource(self.user_id, resource[0])

            # NEW: Download file to user's Downloads folder
            downloads_dir = str(Path.home() / "Downloads")
            os.makedirs(downloads_dir, exist_ok=True)
            filepath = self.db.get_resource_path(resource[0])
            if filepath and os.path.exists(filepath):
                dest_path = os.path.join(downloads_dir, os.path.basename(filepath))
                shutil.copy(filepath, dest_path)
                QMessageBox.information(self, "Success", f"Resource borrowed and saved to {dest_path}")
            else:
                QMessageBox.warning(self, "Error", "Resource file not found.")
