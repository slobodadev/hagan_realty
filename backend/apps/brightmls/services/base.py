import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from odata import ODataService
from authlib.integrations.requests_client import OAuth2Session
from django.conf import settings


class BrightMLSBaseService:
    access_token = None
    service = None
    entity_name = None
    limit = 10000
    offset = 0
    stop = None
    max_workers = 20

    def __init__(self):
        self.auth_url = settings.BRIGHT_MLS_AUTH_URL
        self.api_url = settings.BRIGHT_MLS_API_URL
        self.client_id = settings.BRIGHT_MLS_CLIENT_ID
        self.client_secret = settings.BRIGHT_MLS_CLIENT_SECRET
        self.access_token = None

        # print("-- client_id", self.client_id)
        # print("-- client_secret", self.client_secret)
        # print("-- auth_url", self.auth_url)
        # print("-- api_url", self.api_url)

    def get_oauth_token(self):
        session = OAuth2Session(self.client_id, self.client_secret, scope="clientcred")
        token = session.fetch_token(self.auth_url, grant_type="client_credentials")
        self.access_token = token["access_token"]
        return self.access_token

    def get_client(self):
        if not self.service:
            if not self.access_token:
                self.get_oauth_token()

            session = requests.Session()

            # Configure retries for better fault tolerance
            retries = Retry(
                total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504]
            )
            adapter = HTTPAdapter(
                pool_connections=self.max_workers,
                pool_maxsize=self.max_workers,
                max_retries=retries,
            )

            # Mount the adapter to the session for both HTTP and HTTPS
            session.mount("http://", adapter)
            session.mount("https://", adapter)

            session.headers.update(
                {
                    "User-Agent": "Bright WebAPI/1.0",
                    "Authorization": f"Bearer {self.access_token}",
                }
            )

            self.service = ODataService(
                self.api_url,
                session=session,
                reflect_entities=True,
            )
        return self.service
