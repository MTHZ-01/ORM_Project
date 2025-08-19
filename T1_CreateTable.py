from src.orm.connection import run_query
from src.orm.fields import IntegerField, StringField ,ForeignKey
from src.orm.model import Model

class User(Model):
    id = IntegerField(primary_key=True)  
    name = StringField(max_length=100, nullable=False, default="Default name")
    email = StringField(max_length=100, nullable=False)



class employee(Model):
    # id = IntegerField(primary_key=True)  
    name = StringField(max_length=100 ,default="Default name")
    phonenum = StringField(max_length=100, unique=True)
    user = ForeignKey(User, nullable=True)

# Create the table
# employee.create_table()
# User.create_table()