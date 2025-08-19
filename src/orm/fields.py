from typing import Any, Optional, Type


class Field:
    """
    Base class for all model fields.
    Holds metadata about the column type and optional constraints.
    """
    def __init__(self, column_type: str, primary_key: bool = False, nullable: bool = True, 
                 default: Any = None, unique: bool = False):
        self.column_type = column_type
        self.primary_key = primary_key
        self.nullable = nullable
        self.default = default
        self.unique = unique
        self.name: Optional[str] = None  # set by the metaclass

    def _format_default(self) -> str:
        if isinstance(self.default, str):
            return f"'{self.default}'"
        elif isinstance(self.default, bool):
            return '1' if self.default else '0'
        elif self.default is None:
            return 'NULL'
        return str(self.default)

    def ddl(self, include_auto_increment: bool = False) -> str:
        """
        DDL snippet for field.
        """
        parts = [self.column_type]
        
        # AUTO_INCREMENT should come first for MySQL compatibility
        if include_auto_increment and self.primary_key and self.column_type.upper() == "INTEGER":
            parts.append("AUTO_INCREMENT")
        
        if self.primary_key:
            parts.append("PRIMARY KEY")
        if not self.nullable:
            parts.append("NOT NULL")
        if self.unique:
            parts.append("UNIQUE")
        if self.default is not None:
            parts.append(f"DEFAULT {self._format_default()}")
        return " ".join(parts)


class IntegerField(Field):
    def __init__(self, primary_key: bool = False, nullable: bool = True, 
                 default: Optional[int] = None, unique: bool = False):
        super().__init__(column_type="INTEGER", primary_key=primary_key, 
                         nullable=nullable, default=default, unique=unique)


class StringField(Field):
    def __init__(self, max_length: int = 255, primary_key: bool = False, 
                 nullable: bool = True, default: Optional[str] = None, unique: bool = False):
        super().__init__(column_type=f"VARCHAR({max_length})", primary_key=primary_key, 
                         nullable=nullable, default=default, unique=unique)


class FloatField(Field):
    def __init__(self, primary_key: bool = False, nullable: bool = True, 
                 default: Optional[float] = None, unique: bool = False):
        super().__init__(column_type="FLOAT", primary_key=primary_key, 
                         nullable=nullable, default=default, unique=unique)


class BooleanField(Field):
    def __init__(self, primary_key: bool = False, nullable: bool = True, 
                 default: Optional[bool] = None, unique: bool = False):
        super().__init__(column_type="BOOLEAN", primary_key=primary_key, 
                         nullable=nullable, default=default, unique=unique)


class DateTimeField(Field):
    def __init__(self, primary_key: bool = False, nullable: bool = True, 
                 default: Any = None, unique: bool = False):
        super().__init__(column_type="DATETIME", primary_key=primary_key, 
                         nullable=nullable, default=default, unique=unique)


class ForeignKey(Field):
    def __init__(self, reference_model: Type[Any], nullable: bool = False, unique: bool = False):
        super().__init__(column_type="INTEGER", primary_key=False, 
                         nullable=nullable, unique=unique)
        self.reference_model = reference_model

    def ddl(self, include_auto_increment: bool = False) -> str:
        # ForeignKey doesn't need auto_increment, so we ignore the parameter
        return super().ddl(include_auto_increment)


# Add QueryableMixin for use in Model
class QueryableMixin:
    @classmethod
    def objects(cls):
        from .query import QuerySet
        return QuerySet(cls)