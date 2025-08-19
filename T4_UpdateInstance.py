from src.orm.connection import run_query
from src.orm.fields import IntegerField, StringField ,ForeignKey
from src.orm.model import Model
from T1_CreateTable import User, employee



    
e = employee.objects().get(name = "mohammad")
e.user = User.objects().get(name = "naser")
e.name = "mmd"
e.save()

print(e.id)
print(e.name)
print(e.user)