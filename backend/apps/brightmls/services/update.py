import datetime
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from brightmls import models as bright_models
from brightmls.services.base import BrightMLSBaseService

logger = logging.getLogger("brightmls.services")


class BrightMLSUpdateService(BrightMLSBaseService):
    mapping = {
        "BrightMedia": "MediaModificationTimestamp",
        "BrightMembers": "ModificationTimestamp",
        "BrightOffices": "ModificationTimestamp",
        "BrightOpenHouses": "OpenHouseModificationTimestamp",
        "BrightProperties": "ModificationTimestamp",
        "BuildingName": "BldgNameModificationTimestamp",
        "City": "CtyModificationTimestamp",
        "CityZipCode": "CityZipModificationTimestamp",
        # "Deletion": "DeletionTimestamp", # Not use
        "GreenVerification": "GreenVerificationModificationTimestamp",
        # "History": "PropHistChangeTimestamp",  # Not use
        "Lookup": "ModificationTimestamp",
        "PartyPermissions": "PartyPermModificationTimestamp",
        "PropertyArea": "PropAreaModificationTimestamp",
        "RelatedLookup": "ModificationTimestamp",
        "Room": "RoomModificationTimestamp",
        "School": "SchoolModificationTimestamp",
        "SchoolDistrict": "SchoolDistrictModificationTimestamp",
        # "SchoolElementary": "",
        # "SchoolHigh": "",
        # "SchoolMiddle": "",
        "Subdivision": "LoSubdivisionModificationTimestamp",
        "SysAgentMedia": "SysMediaModificationTimestamp",
        "SysOfficeMedia": "SysMediaModificationTimestamp",
        "SysPartyLicense": "SysPartyLicenseModificationTimestamp",
        "Team": "TeamModificationTimestamp",
        "TeamMember": "TeamMemberModificationTimestamp",
        "Unit": "PropUnitModificationTimestamp",
    }

    def update(self):
        # get the last modification timestamp field name (from the mapping Entity type: field name)

        if self.entity_name:
            if self.entity_name not in self.mapping:
                raise ValueError(f"Entity {self.entity_name} not found in mapping")

            entities_to_process = {self.entity_name: self.mapping[self.entity_name]}
        else:
            entities_to_process = self.mapping

        logger.debug(f"--- entities_to_process {entities_to_process}")

        # return

        # service = self.get_client()

        for entity_name, timestamp_field in entities_to_process.items():
            logger.debug(f"--- processing entity: {entity_name}")

            # get the last modification timestamp (biggest from the Entity's table)
            model = getattr(bright_models, entity_name)
            last_updated_record = (
                model.objects.filter(**{timestamp_field + "__isnull": False})
                .order_by("-" + timestamp_field)
                .first()
            )

            if not last_updated_record:
                logger.warning(
                    f"--- --- WARNING! No records found for {entity_name}, starting from the beginning..."
                )

            last_update = (
                getattr(last_updated_record, timestamp_field)
                if last_updated_record
                else None
            )
            last_update_iso = (
                last_update.isoformat(sep="T")
                if last_update
                else "1970-01-01T00:00:00Z"
            )

            logger.debug(f"--- --- last_update: {last_update_iso}")
            # return

            # PATCH to Nov. 2, 2024, 12:08 p.m.
            # last_update_iso = "2024-11-02T12:08:00Z"

            # self._update_sequential(entity_name, last_update_iso)
            self._update_threaded(entity_name, last_update_iso)

    def _update_sequential(self, entity_name, last_update_iso):
        proceed = True
        offset = 0
        while proceed:
            proceed = self._grab_and_save(
                entity_name, last_update_iso, self.limit, offset
            )
            offset += self.limit

    def _update_threaded(self, entity_name, last_update_iso):
        current_offset = 0

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            while True:
                futures = {}
                for offset in range(
                    current_offset,
                    current_offset + self.limit * self.max_workers,
                    self.limit,
                ):
                    future = executor.submit(
                        self._grab_and_save,
                        entity_name,
                        last_update_iso,
                        self.limit,
                        offset,
                    )
                    futures[future] = offset

                # Move to the next batch
                current_offset += self.limit * self.max_workers

                # Process results as they complete
                more_entities = True
                for future in as_completed(futures):
                    offset = futures[future]
                    try:
                        # Fetch result to check if entities were returned
                        result = future.result()

                        # if at least one thread returns no entities, stop the process
                        more_entities &= result
                    except Exception as exc:
                        logging.error(f"Error at offset {offset}: {exc}")
                        return

                if not more_entities:
                    break  # Stop if no more entities are returned from the API

    def _grab_and_save(
        self, entity_name, last_update_iso, limit: int, offset: int
    ) -> bool:
        """ """
        # logging.debug(f"--- started iteration offset={offset}, limit={limit}")
        entities = self._entities_grab(entity_name, last_update_iso, limit, offset)
        logging.debug(
            f"--- --- got {entity_name}: {len(entities)}, ofst={offset}, lim={limit}"
        )
        if entities:
            self._entities_save(entity_name, entities)
            return True

        return False

    def _entities_grab(self, entity_name, last_update_iso, limit: int, offset: int):
        service = self.get_client()
        entity_resource = service.entities[entity_name]

        timestamp_field = self.mapping[entity_name]

        query = (
            service.query(entity_resource)
            .filter(f"{timestamp_field} gt {last_update_iso}")
            .order_by(timestamp_field)
            .offset(offset)
            .limit(limit)
        )
        entities = query.all()

        return entities

    def _entities_save(self, entity_name, entities):
        model_class = getattr(bright_models, entity_name)

        timestamp_field = self.mapping[entity_name]

        instances = []
        for entity in entities:
            # tsf_value = entity.__dict__["__odata__"][timestamp_field]
            # logger.debug(f"--- --- --- entity timestamp_field {tsf_value}")

            instances.append(model_class.from_python_odata(entity))

        # we need a list of fields of the model
        primary_key_field, fields_to_update = self._get_pk_and_fields(model_class)

        # make a bulk create or update operation
        model_class.objects.bulk_update_or_create(
            instances,
            fields_to_update,
            match_field=primary_key_field,
            batch_size=200,
        )
        # logger.debug("--- --- saved")

    def _get_pk_and_fields(self, model_class):
        fields_to_update = []
        primary_key_field = None
        for field in model_class._meta.get_fields():
            if field.primary_key:
                primary_key_field = field.name
            else:
                fields_to_update.append(field.name)

        # logger.debug(f"--- --- primary_key_field {primary_key_field}")

        return primary_key_field, fields_to_update


# class BrightMLSUpdateService(BrightMLSBaseService):
#     # Service to update by History (not match to the client)
#     last_update_default = datetime.datetime(
#         2024, 11, 1, 0, 0, 0, tzinfo=datetime.timezone.utc
#     )
#
#     def update(self):
#         last_update = self._get_newest_history_datetime()
#         print("--- last_update fetched", last_update)
#
#         # If the last update is lower than specific date, set it to specific date
#         if not last_update or last_update < self.last_update_default:
#             last_update = self.last_update_default
#         print("--- last_update resulted", last_update)
#
#         for entities_block in self._history_entities_iterator(last_update):
#             print(f"--- --- fetched entities_block: {len(entities_block)}")
#             history_instances = []
#             for entity in entities_block:
#                 # print(
#                 #     f"--- --- --- entity.PropHistChangeTimestamp: {entity.PropHistChangeTimestamp}"
#                 # )
#                 if entity.PropHistTableName == "LISTINGS":
#                     if entity.PropHistChangeType == "NEW":
#                         self._listing_create(entity)
#                     elif entity.PropHistChangeType == "PRICE":
#                         self._listing_update_price(entity)
#                     elif entity.PropHistChangeType == "STATUS":
#                         self._listing_update_status(entity)
#                     else:
#                         print(
#                             f"--- --- --- skipping {entity.PropHistChangeType} action from time {entity.PropHistChangeTimestamp}"
#                         )
#
#                 history_instances.append(
#                     bright_models.History.from_python_odata(entity)
#                 )
#
#             # bright_models.History.objects.bulk_create(
#             #     history_instances, batch_size=1000, ignore_conflicts=True
#             # )
#
#     def _get_newest_history_datetime(self):
#         record = bright_models.History.objects.first()
#         if not record:
#             return None
#
#         return record.PropHistChangeTimestamp
#
#     def _history_entities_iterator(self, gt_than_datetime: datetime.datetime):
#         service = self.get_client()
#
#         entity_resource = service.entities["History"]
#
#         while True:
#             if self.offset >= self.stop:
#                 print(f"--- --- stopped by STOP arg: {self.stop}")
#                 break
#
#             print(f"\n--- --- offset:{self.offset}")
#             query = (
#                 service.query(entity_resource)
#                 .filter(
#                     "PropHistChangeTimestamp gt {0}".format(
#                         gt_than_datetime.isoformat(sep="T")
#                     )
#                 )
#                 .order_by("PropHistChangeTimestamp")
#             )
#             query = query.offset(self.offset).limit(self.limit)
#
#             entities = query.all()
#             print(f"--- --- fetched entities: {len(entities)}")
#
#             if not entities:
#                 print(f"--- --- stopped by entities end")
#                 break
#
#             self.offset += self.limit
#
#             yield entities
#
#     def _listing_create(self, entity):
#         print("--- --- --- --- creating NEW listing", entity.PropHistListingKey)
#         # property_entity = (
#         #     self.get_client().entities["BrightProperties"].get(listing_key)
#         # )
#         # print(f"--- --- --- --- exists: {property_entity}")
#         # obj = bright_models.BrightProperties.from_python_odata(property_entity)
#         # obj.save()
#
#     def _listing_update_price(self, entity):
#         print(
#             f"--- --- --- --- updating listing PRICE "
#             f"for #{entity.PropHistListingKey}, "
#             f"column: {entity.PropHistColumnName}, "
#             f"from: {entity.PropHistOriginalColumnValue}, to: {entity.PropHistNewColumnValue}"
#         )
#
#     def _listing_update_status(self, entity):
#         print(
#             f"--- --- --- --- updating listing STATUS "
#             f"for #{entity.PropHistListingKey}, "
#             f"column: {entity.PropHistColumnName}, "
#             f"from: {entity.PropHistOriginalColumnValue}, to: {entity.PropHistNewColumnValue}"
#         )
