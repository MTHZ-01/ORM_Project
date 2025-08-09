from typing import Any, Optional, Type


class Field:
    """
    Base class for all model fields.
    Holds metadata about the column type and optional constraints.
    """
    def __init__(self, column_type: str, primary_key: bool = False, nullable: bool = True, default: Any = None):
        self.column_type = column_type
        self.primary_key = primary_key
        self.nullable = nullable
        self.default = default
        self.name: Optional[str] = None  # set by the metaclass

    def ddl(self) -> str:
        """
        Generate the DDL snippet for this field.
        """
        parts = [self.column_type]
        if self.primary_key:
            parts.append("PRIMARY KEY")
        if not self.nullable:
            parts.append("NOT NULL")
        if self.default is not None:
            parts.append(f"DEFAULT {self._format_default()}")
        return " ".join(parts)

    def _format_default(self) -> str:
        if isinstance(self.default, str):
            return f"'{self.default}'"
        return str(self.default)


class IntegerField(Field):
    def __init__(self, primary_key: bool = False, nullable: bool = True, default: Optional[int] = None):
        super().__init__(column_type="INTEGER", primary_key=primary_key, nullable=nullable, default=default)


class StringField(Field):
    def __init__(self, max_length: int = 255, primary_key: bool = False, nullable: bool = True, default: Optional[str] = None):
        super().__init__(column_type=f"VARCHAR({max_length})", primary_key=primary_key, nullable=nullable, default=default)


class FloatField(Field):
    def __init__(self, primary_key: bool = False, nullable: bool = True, default: Optional[float] = None):
        super().__init__(column_type="FLOAT", primary_key=primary_key, nullable=nullable, default=default)


class BooleanField(Field):
    def __init__(self, primary_key: bool = False, nullable: bool = True, default: Optional[bool] = None):
        super().__init__(column_type="BOOLEAN", primary_key=primary_key, nullable=nullable, default=default)


class DateTimeField(Field):
    def __init__(self, primary_key: bool = False, nullable: bool = True, default: Any = None):
        super().__init__(column_type="DATETIME", primary_key=primary_key, nullable=nullable, default=default)


class ForeignKey(Field):
    def __init__(self, reference_model: Type[Any], nullable: bool = False):
        # store reference model class for relationship handling
        super().__init__(column_type="INTEGER", primary_key=False, nullable=nullable)
        self.reference_model = reference_model

    def ddl(self) -> str:
        # foreign key constraint appended separately by migrations or schema generator
        return super().ddl()


# Add QueryableMixin for use in Model
class QueryableMixin:
    @classmethod
    def objects(cls):
        from .query import QuerySet
        return QuerySet(cls)