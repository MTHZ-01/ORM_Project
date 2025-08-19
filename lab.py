from src.orm.connection import run_query
from src.orm.fields import IntegerField, StringField ,ForeignKey
from src.orm.model import Model

class User(Model):
    id = IntegerField(primary_key=True)  
    name = StringField(max_length=100, nullable=False)
    email = StringField(max_length=100, nullable=False)



class employee(Model):
    # id = IntegerField(primary_key=True)  
    name = StringField(max_length=100)
    phonenum = StringField(max_length=100)
    user = ForeignKey(User)

# Create the table
employee.create_table()
User.create_table()


user = User( name="mmd", email="alice@example.com")
user.save()

u = User.objects().all()[0]
e= employee(name = "MMD", phonenum = "0915", user = u)
e.save()

# Query all users
users = User.objects().all()
emps = employee.objects().all()

for u in users:
    print(f"ID: {u.id}, Name: {u.name}, Email: {u.email}")
    # u.delete()
    
# print()

# userToDelete = employee.objects().get(name = "MMD")

# userToDelete.delete()

# print(f"ID: {userToDelete.id}, Name: {userToDelete.name}, Email: {userToDelete.email}")
# userToDelete.delete()

# for e in emps:
#     # print(f"ID: {e.id}, Name: {e.name}, Email: {e.phonenum}")
#     e.delete()



for e in emps:
    print(f"ID: {e.id}, Name: {e.name}, Email: {e.phonenum}")   
    # e.delete()


# Update user
# user.update(name="Alice Smith")

# Delete user
# user.delete()
