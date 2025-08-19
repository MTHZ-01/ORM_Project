from .fields import IntegerField
from .fields import Field

class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        fields = {}
        primary_keys = []

        # Collect declared fields and primary keys
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                value.name = key
                fields[key] = value
                attrs.pop(key)
                if value.primary_key:
                    primary_keys.append(key)

        # If no primary key defined, add default id
        if not primary_keys:
            id_field = IntegerField()
            id_field.name = "id"
            id_field.primary_key = True
            id_field.auto_increment = True  
            fields["id"] = id_field

        # Validate only one primary key
        if len([f for f in fields.values() if f.primary_key]) > 1:
            raise RuntimeError("Multiple primary keys defined.")

        attrs["_fields"] = fields
        attrs["_table"] = name.lower()
        return super().__new__(cls, name, bases, attrs)
