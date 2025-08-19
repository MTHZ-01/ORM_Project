from src.orm.connection import run_query
from src.orm.fields import IntegerField, StringField ,ForeignKey
from src.orm.model import Model
from T1_CreateTable import User, employee

emps = employee.objects().all()

for e in emps:
    print(f"ID: {e.id}, Name: {e.name}, phoneNum: {e.phonenum} User:{e.user}")   
    print(e.user.name)
    e.delete()

