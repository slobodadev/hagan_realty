import os
import requests
import pyodata
from authlib.integrations.requests_client import OAuth2Session
from brightmls import models as bright_models


class BrightMLSService:
    def __init__(self):
        self.auth_url = os.getenv("BRIGHT_MLS_AUTH_URL")
        self.api_url = os.getenv("BRIGHT_MLS_API_URL")
        self.client_id = os.getenv("BRIGHT_MLS_CLIENT_ID")
        self.client_secret = os.getenv("BRIGHT_MLS_CLIENT_SECRET")
        self.access_token = None

    def get_oauth_token(self):
        """Retrieve OAuth 2.0 access token using client credentials."""
        client = OAuth2Session(self.client_id, self.client_secret)

        # Define the token parameters
        token_params = {
            "grant_type": "client_credentials",
            "scope": "clientcred",
        }

        # Fetch the OAuth 2.0 token
        token = client.fetch_token(self.auth_url, **token_params)
        self.access_token = token["access_token"]
        return self.access_token

    def get_client(self):
        """Create an OData client with OAuth 2.0 token."""
        if not self.access_token:
            self.get_oauth_token()

        # Set up the OData client using pyodata
        session = requests.Session()
        session.headers.update(
            {
                "Authorization": f"Bearer {self.access_token}",
            }
        )

        # Return the OData client
        return pyodata.Client(self.api_url, session)

    # def fetch_entity_data(self, entity_set_name):
    #     """Fetch data from an OData entity set."""
    #     odata_client = self.get_client()
    #     entity_set = odata_client.entity_sets[entity_set_name].get_entities().execute()
    #     return entity_set

    def populate_teams(self):
        """
        populate teams and team members
        """

        client = self.get_client()

        team_entities = client.entity_sets.Team.get_entities().execute()

        for team_entity in team_entities:
            # Save the team (team_lead_member_key will be handled later)
            team_instance = bright_models.Team.from_pyodata(team_entity)
            team_instance.save()

            # Fetch all TeamMember entities associated with this specific team
            team_member_entities = (
                client.entity_sets.TeamMember.get_entities()
                .filter(f"TeamMemberTeamKey eq {team_instance.team_key}")
                .execute()
            )

            # Iterate through the team members and save them
            for team_member_entity in team_member_entities:
                team_member_instance = bright_models.TeamMember.from_pyodata(
                    team_member_entity
                )
                team_member_instance.save()

            # Fix the team_lead_member_key if the lead member exists in the team
            if team_entity.TeamLeadMemberKey:
                lead_member = bright_models.TeamMember.objects.filter(
                    team_member_key=team_entity.TeamLeadMemberKey
                ).first()
                if lead_member:
                    team_instance.team_lead_member_key = lead_member
                    team_instance.save()  # Update the team with the correct lead member
