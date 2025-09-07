import sqlite3
import os

class Database:
    def __init__(self, db_path="data/library.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT UNIQUE,
                password TEXT NOT NULL,
                role TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS resources (
                resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                type TEXT,
                author TEXT,
                filepath TEXT NOT NULL,
                uploaded_by INTEGER,
                FOREIGN KEY(uploaded_by) REFERENCES users(user_id)
            )
        """)
        # Borrowed table for tracking book/resource usage
        cur.execute("""
            CREATE TABLE IF NOT EXISTS borrowed (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                resource_id INTEGER,
                status TEXT,  -- e.g., 'borrowed', 'returned'
                FOREIGN KEY(user_id) REFERENCES users(user_id),
                FOREIGN KEY(resource_id) REFERENCES resources(resource_id)
            )
        """)
        self.conn.commit()

    def add_resource(self, title, type_, author, filepath, teacher_id):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO resources (title, type, author, filepath, uploaded_by) VALUES (?, ?, ?, ?, ?)",
            (title, type_, author, filepath, teacher_id)
        )
        self.conn.commit()

    def get_resources_by_teacher(self, teacher_id):
        cur = self.conn.cursor()
        cur.execute("SELECT resource_id, title, type, author, filepath FROM resources WHERE uploaded_by=?", (teacher_id,))
        return cur.fetchall()

    # NEW: log borrow
    def borrow_resource(self, user_id, resource_id):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO borrowed (user_id, resource_id, status) VALUES (?, ?, ?)",
            (user_id, resource_id, "borrowed")
        )
        self.conn.commit()

    # NEW: log return
    def return_resource(self, user_id, resource_id):
        cur = self.conn.cursor()
        cur.execute(
            "UPDATE borrowed SET status=? WHERE user_id=? AND resource_id=?",
            ("returned", user_id, resource_id)
        )
        self.conn.commit()

    # NEW: fetch usage logs for admin
    def get_usage_logs(self):
        cur = self.conn.cursor()
        cur.execute("SELECT user_id, resource_id, status, id FROM borrowed")
        return cur.fetchall()

    # NEW: fetch resource file path
    def get_resource_path(self, resource_id):
        cur = self.conn.cursor()
        cur.execute("SELECT filepath FROM resources WHERE resource_id=?", (resource_id,))
        row = cur.fetchone()
        return row[0] if row else None
