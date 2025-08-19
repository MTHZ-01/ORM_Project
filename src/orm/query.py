from typing import Any, List
from .connection import run_query


class QuerySet:
    def __init__(self, model_cls: Any):
        self.model_cls = model_cls
        self._where_clauses = []

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


    def all(self) -> List[Any]:
        sql = f"SELECT * FROM {self.model_cls._table}"

        if self._where_clauses:
            where_sql = " AND ".join(self._where_clauses)
            sql += f" WHERE {where_sql}"


        rows = run_query(sql)
        # Use the model's from_row method to properly resolve ForeignKeys
        return [self.model_cls.from_row(row) for row in rows]  # ✅ Change this line


# Optional: helper method for models
class QueryableMixin:
    @classmethod
    def objects(cls) -> QuerySet:
        return QuerySet(cls)
