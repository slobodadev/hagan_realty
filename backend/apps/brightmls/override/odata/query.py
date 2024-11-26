from typing import TypeVar
from odata.query import Query

Q = TypeVar("Q")


class Query(Query):
    def __init__(
        self, entitycls: Q, connection=None, options=None, compound_expand=True
    ):
        super().__init__(entitycls, connection, options, compound_expand)
        print("------------ I AM QueryExtended ------------")

    def _get_options(self):
        options = super()._get_options()

        _skiptoken = self.options.get("$skiptoken")
        if _skiptoken:
            options["$skiptoken"] = _skiptoken

        return options

    def skiptoken(self, value) -> "Query[Q]":
        """
        Set ``$skiptoken`` query parameter

        :param values: Apply string
        :return: Query instance
        """
        q = self._new_query()
        q.options["$skiptoken"] = value
        return q
