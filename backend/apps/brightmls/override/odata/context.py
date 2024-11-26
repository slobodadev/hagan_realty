from brightmls.override.odata.query import Query

from odata.context import Context
from .query import Query


class Context(Context):
    def __init__(self, session=None, auth=None, extra_headers: dict = None):
        super().__init__(session=session, auth=auth, extra_headers=extra_headers)
        print("------------ I AM ContextExtended ------------")

    def query(self, entitycls):
        q = Query(entitycls, connection=self.connection)
        return q
