import os
import re
import requests
from pprint import pprint
from odata import ODataService
from authlib.integrations.requests_client import OAuth2Session
from django.conf import settings
from django.db import connection
from django.utils.dateparse import parse_datetime
from brightmls import models as bright_models


class BrightMLSService:
    entity_name = None
    limit = 10000
    offset = 0
    stop = 10**9

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

        if not isinstance(self.limit, int):
            raise ValueError("Limit must be an integer")
        if not isinstance(self.offset, int):
            raise ValueError("Offset must be an integer")
        if not isinstance(self.stop, int):
            raise ValueError("Stop must be an integer")

    def get_oauth_token(self):
        """Retrieve OAuth 2.0 access token using client credentials."""

        session = OAuth2Session(self.client_id, self.client_secret, scope="clientcred")
        # print("---session", session)

        # Fetch the OAuth 2.0 token
        token = session.fetch_token(self.auth_url, grant_type="client_credentials")
        print("---token", token)

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
                "User-Agent": "Bright WebAPI/1.0",
                "Authorization": f"Bearer {self.access_token}",
            }
        )

        # print("session.headers", session.headers)

        return ODataService(
            self.api_url,
            session=session,
            reflect_entities=True,
            # reflect_output_package="backend.apps.brightmls.entities_cache",
        )

    def populate(self):
        entities = self.get_client().entities

        # pprint(entities)

        try:
            entity_meta = entities[self.entity_name]
        except KeyError:
            raise ValueError(
                f"Entity {self.entity_name} not found. "
                f"Provide the name in camel case as it specified on Bright MLS website"
            )

        # pprint(entity_meta)

        # convert entity name to snake case
        method_name = (
            "populate_" + re.sub(r"(?<!^)(?=[A-Z])", "_", self.entity_name).lower()
        )

        if not hasattr(self, method_name):
            raise NotImplementedError(f"Method {method_name} not implemented yet...")

        getattr(self, method_name)()

    def test(self):
        # print("-- client_id", self.client_id)
        # print("-- client_secret", self.client_secret)
        # print("-- auth_url", self.auth_url)
        #
        # session = OAuth2Session(self.client_id, self.client_secret, scope="clientcred")
        # print("---session", session)
        #
        # token = session.fetch_token(
        #     "https://brightmls.okta.com/oauth2/default/v1/token",
        #     grant_type="client_credentials",
        # )
        # print("--token", token)

        # """Test the BrightMLS service."""
        # client = self.get_client()
        # # team_entities = client.entity_sets.Team.get_entities().execute()
        # # return team_entities

        client = self.get_client()
        # Teams = generated.trippin.Team

        # print("client.entities", client.entities)

        Team = client.entities["Team"]

        # from brightmls.entities_cache import Team

        query = client.query(Team)
        values = query.all()

        # print count of teams
        print(len(values))

        for team in values[:10]:
            print(team)
            # print(client.values(team.TeamLeadMemberKey))

            if team.TeamLeadMemberKey:
                print(client.values(team))
                print(client.values(team.TeamLeadMemberKey))

        # Unit = client.entities["Unit"]
        # query = client.query(Unit)
        # values = query.all()
        #
        # # print count of Unit
        # print(len(values))

        return "test"

    def _entities_iterator(self):
        service = self.get_client()

        print(f"--- Iterating entity: {self.entity_name} ---")

        entity_resource = service.entities[self.entity_name]

        while True:
            if self.offset >= self.stop:
                print(f"--- --- stopped by STOP arg: {self.stop} ---")
                break

            print(f"\n--- --- offset:{self.offset} ---")
            query = service.query(entity_resource)
            query = query.offset(self.offset).limit(self.limit)

            entities = query.all()
            print(f"--- --- fetched entities: {len(entities)}")

            if not entities:
                print(f"--- --- stopped by entities end ---")
                break

            self.offset += self.limit

            yield entities

    def _bulk_create_simple(self, model_class, entities_block):
        instances = []
        for entity in entities_block:
            instances.append(model_class.from_python_odata(entity))

        model_class.objects.bulk_create(
            instances, batch_size=1000, ignore_conflicts=True
        )

    def populate_lookups(self):
        for entities_block in self._entities_iterator("Lookup", limit=10000):
            self._bulk_create_simple(bright_models.Lookup, entities_block)

    def populate_related_lookups(self):
        # clear all related lookups
        # bright_models.RelatedLookup.objects.all().delete()

        for related_lookup_block in self._entities_iterator():
            lookup_ids = [item.LookupKey for item in related_lookup_block]
            lookups = bright_models.Lookup.objects.filter(lookup_key__in=lookup_ids)
            lookup_objects = {lookup.lookup_key: lookup for lookup in lookups}

            instances = []
            for item in related_lookup_block:
                try:
                    lookup = lookup_objects[item.LookupKey]
                except IndexError:
                    print(f"--- --- --- --- Lookup {item.LookupKey} not found!!!")
                    continue

                instances.append(
                    bright_models.RelatedLookup(
                        related_lookup_key=int(item.RelatedLookupKey),
                        lookup_key=lookup,
                        modification_timestamp=item.ModificationTimestamp
                        if item.ModificationTimestamp
                        else None,
                    )
                )

            print(f"--- --- instances appended: {len(instances)}")
            bright_models.RelatedLookup.objects.bulk_create(
                instances,
                batch_size=1000,  # ignore_conflicts=True
            )

            print()

        print(f"- querues count {len(connection.queries)}")
        # print(connection.queries)

    def populate_city(self):
        for entities_block in self._entities_iterator():
            self._bulk_create_simple(bright_models.City, entities_block)

    def populate_city_zip_code(self):
        # bright_models.CityZipCode.objects.all().delete()

        for entities_block in self._entities_iterator():
            city_ids = [item.CityZipCodeCity for item in entities_block]
            cities = bright_models.City.objects.filter(cty_city_key__in=city_ids)
            city_objects = {city.cty_city_key: city for city in cities}

            for index, item in enumerate(entities_block):
                try:
                    entities_block[index].CityZipCodeCity = city_objects[
                        item.CityZipCodeCity
                    ]
                except IndexError:
                    print(f"--- --- --- --- City {item.CityZipCodeCity} not found!!!")
                    continue

            self._bulk_create_simple(bright_models.CityZipCode, entities_block)

    # def populate_teams(self):
    #     """
    #     populate teams and team members
    #     """
    #
    #     service = self.get_client()
    #
    #     Team = service.entities["Team"]
    #     TeamMember = service.entities["TeamMember"]
    #
    #     # get all teams
    #     query = service.query(Team)
    #     teams = query.all()
    #
    #     team_instances = []
    #     for team in teams[:10]:
    #         # Create a team instance without saving it
    #         # team_instances.append(bright_models.Team.from_pyodata(team))
    #
    #     team_objects = bright_models.Team.objects.bulk_create(
    #         team_instances, batch_size=200
    #     )
    #
    #     return team_objects
    #
    #     client = self.get_client()
    #
    #     team_entities = client.entity_sets.Team.get_entities().execute()
    #
    #     for team_entity in team_entities:
    #         # Save the team (team_lead_member_key will be handled later)
    #         team_instance = bright_models.Team.from_pyodata(team_entity)
    #         team_instance.save()
    #
    #         # Fetch all TeamMember entities associated with this specific team
    #         team_member_entities = (
    #             client.entity_sets.TeamMember.get_entities()
    #             .filter(f"TeamMemberTeamKey eq {team_instance.team_key}")
    #             .execute()
    #         )
    #
    #         # Iterate through the team members and save them
    #         for team_member_entity in team_member_entities:
    #             team_member_instance = bright_models.TeamMember.from_pyodata(
    #                 team_member_entity
    #             )
    #             team_member_instance.save()
    #
    #         # Fix the team_lead_member_key if the lead member exists in the team
    #         if team_entity.TeamLeadMemberKey:
    #             lead_member = bright_models.TeamMember.objects.filter(
    #                 team_member_key=team_entity.TeamLeadMemberKey
    #             ).first()
    #             if lead_member:
    #                 team_instance.team_lead_member_key = lead_member
    #                 team_instance.save()  # Update the team with the correct lead member
