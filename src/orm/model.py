from typing import Any, Dict, Type, List

""" Connection to the database 👇"""
from .connection import run_query

from .metaclass import ModelMeta
from .query import QueryableMixin


class Model(QueryableMixin, metaclass=ModelMeta):
    """
    CRUD methods and model initialization.
    """

    def __init__(self, **kwargs):
        for field_name, field in self._fields.items():
            value = kwargs.get(field_name, field.default)
            setattr(self, field_name, value)

    def save(self):
        columns = []
        values = []
        placeholders = []

        for name, field in self._fields.items():
            val = getattr(self, name)
            if field.primary_key and val is None:
                continue  # Let DB handle auto-increment PK
            columns.append(name)
            values.append(val)
            placeholders.append("%s")

        cols_sql = ", ".join(columns)
        ph_sql = ", ".join(placeholders)
        sql = f"INSERT INTO {self._table} ({cols_sql}) VALUES ({ph_sql})"
        
        # Execute and get last insert ID
        last_id = run_query(sql % tuple(map(repr, values)), return_last_id=True)
        pk_field = self.get_primary_key_field()
        setattr(self, pk_field.name, last_id)

    def update(self, **kwargs):
        """Update fields of this model instance in the database."""
        assignments = []
        values = []

        for k, v in kwargs.items():
            assignments.append(f"{k} = %s")
            values.append(v)
            setattr(self, k, v)

        pk_field = self.get_primary_key_field()
        values.append(getattr(self, pk_field.name))

        set_sql = ", ".join(assignments)
        sql = f"UPDATE {self._table} SET {set_sql} WHERE {pk_field.name} = %s"
        run_query(sql % tuple(map(repr, values)))

    def delete(self):
        """Delete this model instance from the database."""
        pk_field = self.get_primary_key_field()
        pk_value = getattr(self, pk_field.name)
        sql = f"DELETE FROM {self._table} WHERE {pk_field.name} = %s"
        run_query(sql % repr(pk_value))

    @classmethod
    def all(cls) -> List["Model"]:
        sql = f"SELECT * FROM {cls._table}"
        rows = run_query(sql)
        return [cls(**row) for row in rows]

    @classmethod
    def filter(cls, **conditions) -> List["Model"]:
        where_clauses = []
        values = []

        for k, v in conditions.items():
            where_clauses.append(f"{k} = %s")
            values.append(v)

        where_sql = " AND ".join(where_clauses)
        sql = f"SELECT * FROM {cls._table} WHERE {where_sql}"
        rows = run_query(sql % tuple(map(repr, values)))
        return [cls(**row) for row in rows]

    @classmethod
    def create_table(cls):
        """Generate and run CREATE TABLE statement for this model."""
        cols = []
        for name, field in cls._fields.items():
            ddl = field.ddl()
            if field.primary_key and field.column_type.upper() == "INTEGER":
                ddl += " AUTO_INCREMENT"
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
