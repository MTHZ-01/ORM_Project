from src.orm.connection import run_query
from src.orm.fields import IntegerField, StringField, ForeignKey
from src.orm.model import Model
from T1_CreateTable import User, employee

user = User(email="mmd@example.com")
user.save()

user = User(name="mobin", email="mobin@example.com")
user.save()

user = User(name="naser", email="naser@example.com")
user.save()



u = User.objects().get(name = "mobin")
e= employee(name = "mohammad", phonenum = "0915", user = u)
e.save()


e= employee(name = "nima", phonenum = "0936", user = u)
e.save()
