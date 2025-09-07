# backend/models.py
from backend.database import Database

class User:
    def __init__(self, user_id, name, email, role="student"):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role

    def __repr__(self):
        return f"<User {self.name} ({self.role})>"

class Student(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email, role="student")

class Teacher(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email, role="teacher")

class Resource:
    def __init__(self, resource_id, title, author, res_type, filename=None):
        self.resource_id = resource_id
        self.title = title
        self.author = author
        self.type = res_type
        self.filename = filename

    def __repr__(self):
        return f"<Resource {self.title} ({self.type})>"

class LibrarySystem:
    def __init__(self, db: Database):
        self.db = db

    # user helpers
    def register_user(self, name, email, password, role="student"):
        row = self.db.add_user(name, email, password, role)
        if row:
            return User(row["user_id"], row["name"], row["email"], row["role"])
        return None

    def login_user(self, email, password):
        row = self.db.get_user_by_email(email)
        if row and row["password"] == password:
            return User(row["user_id"], row["name"], row["email"], row["role"])
        return None

    # resource helpers
    def upload_resource(self, title, author, res_type, source_filepath, uploaded_by):
        rid = self.db.add_resource(title, author, res_type, source_filepath, uploaded_by)
        return rid

    def search_resources(self, q="", res_type=None):
        rows = self.db.search_resources(q, res_type)
        resources = []
        for r in rows:
            resources.append(Resource(r["resource_id"], r["title"], r["author"], r["type"], r["filename"]))
        return resources

    def borrow(self, user_id, resource_id):
        return self.db.borrow_resource(user_id, resource_id)

    def return_resource(self, user_id, resource_id):
        return self.db.return_resource(user_id, resource_id)

    def get_user_borrowed(self, user_id):
        return self.db.get_user_borrowed(user_id)

    def list_all_resources(self):
        rows = self.db.list_resources()
        out = []
        for r in rows:
            out.append(Resource(r["resource_id"], r["title"], r["author"], r["type"], r["filename"]))
        return out

    def delete_resource(self, resource_id):
        self.db.delete_resource(resource_id)

    def get_all_borrow_logs(self):
        return self.db.get_all_borrow_logs()
