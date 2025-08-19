from typing import Any, Dict, Type, List
from .fields import ForeignKey

""" Connection to the database 👇"""
from .connection import run_query

from .metaclass import ModelMeta
from .query import QueryableMixin


class Model(QueryableMixin, metaclass=ModelMeta):
    """
    CRUD methods and model initialization.
    """

    def __str__(self):
        # Return a more meaningful string representation
        pk_field = self.get_primary_key_field()
        pk_value = getattr(self, pk_field.name)
        return f"<{self.__class__.__name__}: {pk_value}>"

    def __repr__(self):
        # This will be shown when you print the object directly
        return self.__str__()

    def __init__(self, **kwargs):
        for field_name, field in self._fields.items():
            value = kwargs.get(field_name, field.default)
            setattr(self, field_name, value)

    def save(self):
        pk_field = self.get_primary_key_field()
        pk_value = getattr(self, pk_field.name)

        # Check for unique constraint violations before saving
        self._check_unique_constraints(pk_value)

        if pk_value is None:
            # INSERT
            columns = []
            values = []
            placeholders = []

            for name, field in self._fields.items():
                val = getattr(self, name)
                
                # Skip primary key if it's None (auto-increment)
                if field.primary_key and val is None:
                    continue
                
                # Handle nullable fields
                if val is None:
                    if not field.nullable:
                        if field.default is not None:
                            # Use default value for non-nullable fields
                            val = field.default
                        else:
                            raise ValueError(f"Field '{name}' cannot be null")
                    # For nullable fields, we keep None value
                elif isinstance(field, ForeignKey) and val is not None:
                    # Convert ForeignKey object to its primary key value
                    pk_f = field.reference_model.get_primary_key_field()
                    val = getattr(val, pk_f.name)
                
                columns.append(name)
                values.append(val)
                placeholders.append("%s")

            cols_sql = ", ".join(columns)
            ph_sql = ", ".join(placeholders)
            sql = f"INSERT INTO {self._table} ({cols_sql}) VALUES ({ph_sql})"

            last_id = run_query(sql, params=tuple(values), return_last_id=True)
            setattr(self, pk_field.name, last_id)
        else:
            # UPDATE
            assignments = []
            values = []

            for name, field in self._fields.items():
                if field.primary_key:
                    continue
                    
                val = getattr(self, name)
                
                # Handle nullable fields in UPDATE
                if val is None:
                    if not field.nullable:
                        if field.default is not None:
                            # Use default value for non-nullable fields
                            val = field.default
                        else:
                            raise ValueError(f"Field '{name}' cannot be null")
                    # For nullable fields, we keep None value
                elif isinstance(field, ForeignKey) and val is not None:
                    # Convert ForeignKey object to its primary key value
                    pk_f = field.reference_model.get_primary_key_field()
                    val = getattr(val, pk_f.name)
                
                assignments.append(f"{name} = %s")
                values.append(val)

            values.append(pk_value)
            set_sql = ", ".join(assignments)
            sql = f"UPDATE {self._table} SET {set_sql} WHERE {pk_field.name} = %s"
            run_query(sql, params=tuple(values))

    def _check_unique_constraints(self, current_pk_value):
        """Check if any unique constraints would be violated by saving this object."""
        # Get the primary key field for the current model
        pk_field = self.get_primary_key_field()
        
        for name, field in self._fields.items():
            if field.unique:
                value = getattr(self, name)
                
                # Skip None values for unique fields (they don't violate unique constraint)
                if value is None:
                    continue
                    
                # For ForeignKey fields, get the actual PK value
                if isinstance(field, ForeignKey) and value is not None:
                    pk_f = field.reference_model.get_primary_key_field()
                    value = getattr(value, pk_f.name)
                
                # Check if another object already has this value
                existing_objects = self.__class__.objects().filter(**{name: value})
                
                for obj in existing_objects:
                    # Skip the current object if we're updating
                    if current_pk_value is not None and getattr(obj, pk_field.name) == current_pk_value:
                        continue
                        
                    # If we found another object with the same value, raise error
                    raise ValueError(f"Unique constraint violation: {name}='{value}' already exists")

    def delete(self):
        """Delete this model instance from the database."""
        pk_field = self.get_primary_key_field()
        pk_value = getattr(self, pk_field.name)
        sql = f"DELETE FROM {self._table} WHERE {pk_field.name} = %s"
        run_query(sql % repr(pk_value))

    @classmethod
    def from_row(cls, row: dict):
        """Convert DB row to Model instance with ForeignKeys resolved."""
        kwargs = {}
        for name, field in cls._fields.items():
            value = row.get(name)
            if isinstance(field, ForeignKey) and value is not None:
                # پیدا کردن مدل رفرنس
                ref_model = field.reference_model
                ref_pk = ref_model.get_primary_key_field().name
                # گرفتن آبجکت کامل
                ref_obj = ref_model.filter(**{ref_pk: value})
                kwargs[name] = ref_obj[0] if ref_obj else None
            else:
                kwargs[name] = value
        return cls(**kwargs)

    @classmethod
    def all(cls) -> List["Model"]:
        sql = f"SELECT * FROM {cls._table}"
        rows = run_query(sql)
        return [cls.from_row(row) for row in rows]  

    @classmethod
    def filter(cls, **conditions) -> List["Model"]:
        where_clauses = []
        values = []

        for k, v in conditions.items():
            where_clauses.append(f"{k} = %s")
            # اگر foreign key object پاس داده باشیم
            field = cls._fields.get(k)
            if isinstance(field, ForeignKey) and v is not None:
                pk_field = field.reference_model.get_primary_key_field()
                v = getattr(v, pk_field.name)
            values.append(v)

        where_sql = " AND ".join(where_clauses)
        sql = f"SELECT * FROM {cls._table} WHERE {where_sql}"
        rows = run_query(sql, params=tuple(values))
        return [cls.from_row(row) for row in rows]

    @classmethod
    def create_table(cls):
        """Generate and run CREATE TABLE statement for this model."""
        cols = []
        for name, field in cls._fields.items():
            # For unique fields, we need to handle them differently in some databases
            ddl = field.ddl(include_auto_increment=True)
            cols.append(f"{name} {ddl}")

        cols_sql = ", ".join(cols)
        sql = f"CREATE TABLE IF NOT EXISTS {cls._table} ({cols_sql});"
        run_query(sql)

    @classmethod
    def get_primary_key_field(cls) -> Any:
        for field in cls._fields.values():
            if field.primary_key:
                return field
        raise RuntimeError(f"No primary key defined for table {cls._table}")
