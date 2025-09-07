import os
from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout,
                             QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem)
from PyQt6.QtCore import Qt
from backend.database import Database


class TeacherDashboard(QWidget):
    def __init__(self, teacher_id, logout_callback):
        super().__init__()
        self.teacher_id = teacher_id
        self.logout_callback = logout_callback
        self.db = Database("data/library.db")

        self.setWindowTitle("Teacher Dashboard - Digital Library")
        self.setFixedSize(600, 400)

        self.init_ui()
        self.load_resources()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("📖 Teacher Dashboard")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)

        # Upload button
        upload_btn = QPushButton("Upload Resource")
        upload_btn.setStyleSheet("background:#4CAF50; color:white; padding:6px; border-radius:6px;")
        upload_btn.clicked.connect(self.upload_resource)
        layout.addWidget(upload_btn)

        # Table to show resources
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Title", "File Path"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        # NEW: Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("background:#f44336; color:white; padding:5px; border-radius:6px;")
        logout_btn.clicked.connect(self.logout_callback)
        layout.addWidget(logout_btn)

        self.setLayout(layout)

    def upload_resource(self):
        file_dialog = QFileDialog()
        filepath, _ = file_dialog.getOpenFileName(self, "Select Resource")

        if filepath:
            title = os.path.basename(filepath)
            try:
                # pass type_ and author with default values
                self.db.add_resource(title, "document", "unknown", filepath, self.teacher_id)
                QMessageBox.information(self, "Success", f"Uploaded: {title}")
                self.load_resources()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Upload failed: {e}")

    def load_resources(self):
        resources = self.db.get_resources_by_teacher(self.teacher_id)
        self.table.setRowCount(len(resources))

        for row, res in enumerate(resources):
            self.table.setItem(row, 0, QTableWidgetItem(res[1]))  # title
            self.table.setItem(row, 1, QTableWidgetItem(res[2]))  # filepath
