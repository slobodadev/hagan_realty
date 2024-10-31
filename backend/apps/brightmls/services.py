import os
import re
import requests
import logging
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

        pprint(entities)

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
            print("=== Warning, method not found, use default behavior! ===")

            for entities_block in self._entities_iterator():
                if len(entities_block) == 1:
                    pprint(entities_block[0].__dict__)
                self._bulk_create_simple(
                    getattr(bright_models, self.entity_name), entities_block
                )
        else:
            getattr(self, method_name)()

    def _entities_iterator(self):
        service = self.get_client()

        print(f"--- Iterating entity: {self.entity_name}")

        entity_resource = service.entities[self.entity_name]

        while True:
            if self.offset >= self.stop:
                print(f"--- --- stopped by STOP arg: {self.stop}")
                break

            print(f"\n--- --- offset:{self.offset}")
            query = service.query(entity_resource)
            query = query.offset(self.offset).limit(self.limit)

            entities = query.all()
            print(f"--- --- fetched entities: {len(entities)}")

            if not entities:
                print(f"--- --- stopped by entities end")
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

    # def populate_bright_properties(self):
    #     bright_models.BrightProperties.objects.all().delete()

    #     for entities_block in self._entities_iterator():
    #         for item in entities_block:
    #             print(item.__dict__)
    #             for field in bright_models.BrightProperties._meta.get_fields():
    #                 # model_m_l = getattr(field, "max_length", "Not Supported")
    #                 # model_data = f"{field.name}, {type(field)}({model_m_l})"
    #
    #                 if hasattr(item, field.name):
    #                     value = getattr(item, field.name)
    #                     warning = ""
    #                     if isinstance(value, str):
    #                         value_len = len(value)
    #                         max_len = getattr(field, "max_length", 0)
    #                         warning = (
    #                             f" - WARNING: {value_len} > {max_len}"
    #                             if value_len > max_len
    #                             else ""
    #                         )
    #
    #                     print("- field.name", field.name, "- dat value", value, warning)
    #                 # item_data = (
    #                 #     f" - {len(getattr(item,field.name))}"
    #                 #     if hasattr(item, field.name) and getattr(item, field.name)
    #                 #     else " - None"
    #                 # )
    #                 # # print(field.name, type(field), f" -- {model_m_l}")
    #                 # # print(item.Location)
    #                 # print(model_data, item_data)
    #             return
    #         # self._bulk_create_simple(bright_models.Lookup, entities_block)

    # def populate_related_lookups(self):
    #     # clear all related lookups
    #     # bright_models.RelatedLookup.objects.all().delete()
    #
    #     for related_lookup_block in self._entities_iterator():
    #         lookup_ids = [item.LookupKey for item in related_lookup_block]
    #         lookups = bright_models.Lookup.objects.filter(lookup_key__in=lookup_ids)
    #         lookup_objects = {lookup.lookup_key: lookup for lookup in lookups}
    #
    #         instances = []
    #         for item in related_lookup_block:
    #             try:
    #                 lookup = lookup_objects[item.LookupKey]
    #             except IndexError:
    #                 print(f"--- --- --- --- Lookup {item.LookupKey} not found!!!")
    #                 continue
    #
    #             instances.append(
    #                 bright_models.RelatedLookup(
    #                     related_lookup_key=int(item.RelatedLookupKey),
    #                     lookup_key=lookup,
    #                     modification_timestamp=item.ModificationTimestamp
    #                     if item.ModificationTimestamp
    #                     else None,
    #                 )
    #             )
    #
    #         print(f"--- --- instances appended: {len(instances)}")
    #         bright_models.RelatedLookup.objects.bulk_create(
    #             instances,
    #             batch_size=1000,  # ignore_conflicts=True
    #         )
    #
    #         print()
    #
    #     print(f"- querues count {len(connection.queries)}")
    #     # print(connection.queries)
    #
    # def populate_city(self):
    #     for entities_block in self._entities_iterator():
    #         self._bulk_create_simple(bright_models.City, entities_block)
    #
    # def populate_city_zip_code(self):
    #     # bright_models.CityZipCode.objects.all().delete()
    #
    #     for entities_block in self._entities_iterator():
    #         city_ids = [item.CityZipCodeCity for item in entities_block]
    #         cities = bright_models.City.objects.filter(cty_city_key__in=city_ids)
    #         city_objects = {city.cty_city_key: city for city in cities}
    #
    #         for index, item in enumerate(entities_block):
    #             try:
    #                 entities_block[index].CityZipCodeCity = city_objects[
    #                     item.CityZipCodeCity
    #                 ]
    #             except IndexError:
    #                 print(f"--- --- --- --- City {item.CityZipCodeCity} not found!!!")
    #                 continue
    #
    #         self._bulk_create_simple(bright_models.CityZipCode, entities_block)
    #
    # def populate_builder_model(self):
    #     """
    #     FIXME - entity not found in metadata...
    #     """
    #     for entities_block in self._entities_iterator():
    #         self._bulk_create_simple(bright_models.BuilderModel, entities_block)
    #
    # def populate_building_name(self):
    #     self_relations = {}
    #     for entities_block in self._entities_iterator():
    #         for item in entities_block:
    #             if item.BldgNameRelatedBldgNameKey:
    #                 self_relations[item.BldgNameKey] = item.BldgNameRelatedBldgNameKey
    #
    #         self._bulk_create_simple(bright_models.BuildingName, entities_block)
    #
    #     # update self relations
    #     print("--- --- count of self relations", len(self_relations))
    #     for key, value in self_relations.items():
    #         related = bright_models.BuildingName.objects.filter(
    #             bldg_name_key=value
    #         ).first()
    #
    #         if not related:
    #             print(
    #                 f"--- --- --- --- Related BuildingName #{value} not found for BuildingName #{key}!!!"
    #             )
    #             continue
    #
    #         bright_models.BuildingName.objects.filter(bldg_name_key=key).update(
    #             bldg_name_related_bldg_name_key=related
    #         )
    #
    # def populate_bright_media(self):
    #     for entities_block in self._entities_iterator():
    #         # for item in entities_block:
    #         #     pprint(item.__dict__)
    #         self._bulk_create_simple(bright_models.BrightMedia, entities_block)
    #
    # def populate_bright_members(self):
    #     # bright_models.BrightMember.objects.all().delete()
    #
    #     for entities_block in self._entities_iterator():
    #         # for item in entities_block:
    #         #     # pprint(type(item.__dict__["__odata__"]))
    #         #     pprint(item.__dict__["__odata__"])
    #         #     print(
    #         #         "------- item.MemberPreferredFirstName",
    #         #         item.MemberPreferredFirstName,
    #         #     )
    #         self._bulk_create_simple(bright_models.BrightMember, entities_block)
    #
    # def populate_bright_offices(self):
    #     for entities_block in self._entities_iterator():
    #         # for item in entities_block:
    #         #     pprint(item.__dict__)
    #         self._bulk_create_simple(bright_models.BrightOffice, entities_block)
    #
    # def populate_bright_open_houses(self):
    #     for entities_block in self._entities_iterator():
    #         # for item in entities_block:
    #         #     pprint(item.__dict__)
    #         self._bulk_create_simple(bright_models.BrightOpenHouse, entities_block)
