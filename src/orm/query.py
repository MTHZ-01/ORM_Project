from typing import Any, List
from .connection import run_query


class QuerySet:
    def __init__(self, model_cls: Any):
        self.model_cls = model_cls
        self._where_clauses = []
        self._order_by = None
        self._limit = None

    def filter(self, **conditions) -> List[Any]:
        for k, v in conditions.items():
            clause = f"{k} = '{v}'"
            self._where_clauses.append(clause)
        return self.all()

    def get(self, **conditions):
        for k, v in conditions.items():
            clause = f"{k} = '{v}'"
            self._where_clauses.append(clause)
        if self.all():
            return self.all()[0]
        return None

    def order_by(self, field_name: str) -> List[Any]:
        self._order_by = field_name
        return self.all()

    def limit(self, count: int) -> List[Any]:
        self._limit = count
        return self.all()

    def all(self) -> List[Any]:
        sql = f"SELECT * FROM {self.model_cls._table}"

        if self._where_clauses:
            where_sql = " AND ".join(self._where_clauses)
            sql += f" WHERE {where_sql}"

        if self._order_by:
            sql += f" ORDER BY {self._order_by}"

        if self._limit is not None:
            sql += f" LIMIT {self._limit}"

        rows = run_query(sql)
        return [self.model_cls(**row) for row in rows]


# Optional: helper method for models
class QueryableMixin:
    @classmethod
    def objects(cls) -> QuerySet:
        return QuerySet(cls)
