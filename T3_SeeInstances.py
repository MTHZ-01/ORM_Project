from src.orm.connection import run_query
from src.orm.fields import IntegerField, StringField ,ForeignKey
from src.orm.model import Model
from T1_CreateTable import User, employee

# Query all users
users = User.objects().all()
emps = employee.objects().all()

for u in users:
    print(f"ID: {u.id}, Name: {u.name}, Email: {u.email}")
#      u.delete()
    
print()

for e in emps:
    print(f"ID: {e.id}, Name: {e.name}, phoneNum: {e.phonenum} User:{e.user}")   
    print(e.user.name)

