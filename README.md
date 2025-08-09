## The ORM Project for database 

# 📂 Project Structure

📦 **Project Root**  
├── `.coverage`  
├── `lab.py`  
│  
├── 📂 **src**  
│   └── 📂 **orm**  
│       ├── `connection.py`  
│       ├── `fields.py`  
│       ├── `metaclass.py`  
│       ├── `model.py`  
│       ├── `query.py`  
│       ├── `Readme.md`  
│       │  
│       └── 📂 `__pycache__`  
│           ├── `connection.cpython-310.pyc`  
│           ├── `fields.cpython-310.pyc`  
│           ├── `metaclass.cpython-310.pyc`  
│           ├── `model.cpython-310.pyc`  
│           ├── `query.cpython-310.pyc`  
│           └── `__init__.cpython-310.pyc`  
│  
└── 📂 **test**

# test_models.py
"""
Unit tests for ORM models (User and Employee)
Demonstrates create, insert, query, and delete operations.
"""

from src.orm.fields import IntegerField, StringField
from src.orm.model import Model


# --------------------
# Model Definitions
# --------------------
class User(Model):
    id = IntegerField(primary_key=True)
    name = StringField(max_length=100, nullable=False)
    email = StringField(max_length=100, nullable=False)


class Employee(Model):
    id = IntegerField(primary_key=True)
    name = StringField(max_length=100, nullable=False)
    phone_number = StringField(max_length=100, nullable=False)


# --------------------
# Unit Test Workflow
# --------------------
if __name__ == "__main__":
    # 1. Create tables (only needed once)
    User.create_table()
    Employee.create_table()

    # 2. Insert sample records
    u1 = User(name="Alice", email="alice@example.com")
    u1.save()

    e1 = Employee(name="MMD", phone_number="0915")
    e1.save()

    # 3. Query all records
    print("\n--- All Users ---")
    for u in User.objects().all():
        print(f"ID: {u.id}, Name: {u.name}, Email: {u.email}")

    print("\n--- All Employees ---")
    for e in Employee.objects().all():
        print(f"ID: {e.id}, Name: {e.name}, Phone: {e.phone_number}")

    # 4. Get a specific record
    print("\n--- Get Employee by Name ---")
    employee_to_delete = Employee.objects().get(name="MMD")
    print(f"Found: ID {employee_to_delete.id}, Name: {employee_to_delete.name}")

    # 5. Delete the record
    employee_to_delete.delete()
    print(f"Deleted Employee: {employee_to_delete.name}")
