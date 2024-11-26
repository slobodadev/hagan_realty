import rich
from typing import Optional, TypeVar
from odata import ODataService

from .query import Query
from .context import Context


class ODataService(ODataService):
    def __init__(
        self,
        url: str,
        base=None,
        reflect_entities: Optional[bool] = None,
        reflect_output_package: Optional[str] = None,
        session=None,
        extra_headers: dict = None,
        auth=None,
        console: rich.console.Console = None,
        quiet_progress: bool = False,
    ):
        super().__init__(
            url,
            base,
            reflect_entities,
            reflect_output_package,
            session,
            extra_headers,
            auth,
            console,
            quiet_progress,
        )
        self.default_context = Context(
            auth=auth, session=session, extra_headers=extra_headers
        )
        print("------------ I AM ODataServiceExtended ------------")

    def create_context(self, auth=None, session=None, extra_headers: dict = None):
        """
        Create new context to use for session-like usage

        :param auth: Custom Requests auth object to use for credentials
        :param session: Custom Requests session to use for communication with the endpoint
        :param extra_headers: Any extra headers to pass to use for all communications
        :return: Context instance
        :rtype: Context
        """
        return Context(auth=auth, session=session, extra_headers=extra_headers)
