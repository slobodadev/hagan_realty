import requests
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from odata import ODataService
from authlib.integrations.requests_client import OAuth2Session
from django.conf import settings


class BrightMLSSession(requests.Session):
    """
    Session class for Bright MLS API with OAuth2 token management.
    The session will automatically refresh the token when it expires.
    It was done because of systematic errors with the previous implementation.
    """

    def __init__(self, maxpagesize=10000):
        """
        Initialize the BrightMLSSession instance.

        :param maxpagesize: The maximum page size for API requests, default is 100.
        """
        super().__init__()
        self.token_url = settings.BRIGHT_MLS_AUTH_URL
        self.client_id = settings.BRIGHT_MLS_CLIENT_ID
        self.client_secret = settings.BRIGHT_MLS_CLIENT_SECRET
        self.maxpagesize = maxpagesize
        self.access_token = None
        self.token_expires_at = None

        # Internal OAuth2 session for token management
        self.oauth_session = OAuth2Session(
            client_id=self.client_id, client_secret=self.client_secret
        )
        self._fetch_token()

        # # Configure retries for better fault tolerance
        # retries = Retry(
        #     total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504]
        # )
        # adapter = HTTPAdapter(
        #     pool_connections=self.max_workers,
        #     pool_maxsize=self.max_workers,
        #     max_retries=retries,
        # )
        #
        # # Mount the adapter to the session for both HTTP and HTTPS
        # session.mount("http://", adapter)
        # session.mount("https://", adapter)

    def _fetch_token(self):
        """
        Fetch a new access token and update the session.
        """
        # print(f">> fetching token...")
        token = self.oauth_session.fetch_token(
            self.token_url, grant_type="client_credentials"
        )
        self.access_token = token["access_token"]
        self.token_expires_at = time.time() + (
            token.get("expires_in", 3600) - 120
        )  # 2 minute buffer
        # self.token_expires_at = time.time() + 10  # dirty test

    def _ensure_token_valid(self):
        """
        Ensure the token is still valid, and refresh it if necessary.
        """
        if not self.access_token or time.time() >= self.token_expires_at:
            print("TR", end="", flush=True)
            self._fetch_token()

    def prepare_request(self, request):
        """
        Override to inject headers into every request.
        """
        self._ensure_token_valid()
        request.headers.update(
            {
                "User-Agent": "Bright WebAPI/1.0",
                "Authorization": f"Bearer {self.access_token}",
                "Prefer": f"odata.maxpagesize={self.maxpagesize}",
            }
        )
        return super().prepare_request(request)


class BrightMLSBaseService:
    access_token = None
    service = None
    entity_name = None
    limit = 10000
    offset = 0
    stop = None
    max_workers = 20

    def __init__(self):
        self.api_url = settings.BRIGHT_MLS_API_URL

    def get_client(self):
        session = BrightMLSSession(maxpagesize=self.limit)

        service = ODataService(
            self.api_url,
            session=session,
            reflect_entities=True,
        )

        return service
