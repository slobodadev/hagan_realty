import datetime
from brightmls import models as bright_models
from brightmls.services.base import BrightMLSBaseService


# class BrightMLSUpdateService(BrightMLSBaseService):
#     mapping = {
#         "BrightMedia": "MediaModificationTimestamp",
#         "BrightMembers": "ModificationTimestamp",
#         "BrightOffices": "ModificationTimestamp",
#         "BrightOpenHouses": "OpenHouseModificationTimestamp",
#         "BrightProperties": "ModificationTimestamp",
#         "BuildingName": "BldgNameModificationTimestamp",
#         "City": "CtyModificationTimestamp",
#         "CityZipCode": "CityZipModificationTimestamp",
#         # "Deletion": "DeletionTimestamp", # Not use
#         "GreenVerification": "GreenVerificationModificationTimestamp",
#         # "History": "PropHistChangeTimestamp",  # Not use
#         "Lookup": "ModificationTimestamp",
#         "PartyPermissions": "PartyPermModificationTimestamp",
#         "PropertyArea": "PropAreaModificationTimestamp",
#         "RelatedLookup": "ModificationTimestamp",
#         "Room": "RoomModificationTimestamp",
#         "School": "SchoolModificationTimestamp",
#         "SchoolDistrict": "SchoolDistrictModificationTimestamp",
#         # "SchoolElementary": "",
#         # "SchoolHigh": "",
#         # "SchoolMiddle": "",
#         "Subdivision": "LoSubdivisionModificationTimestamp",
#         "SysAgentMedia": "SysMediaModificationTimestamp",
#         "SysOfficeMedia": "SysMediaModificationTimestamp",
#         "SysPartyLicense": "SysPartyLicenseModificationTimestamp",
#         "Team": "TeamModificationTimestamp",
#         "TeamMember": "TeamMemberModificationTimestamp",
#         "Unit": "PropUnitModificationTimestamp",
#     }
#
#     def update1(self):
#         # get the last modification timestamp field name (from the mapping Entity type: field name)
#
#         if self.entity_name:
#             if self.entity_name not in self.mapping:
#                 raise ValueError(f"Entity {self.entity_name} not found in mapping")
#
#             entities_to_process = {self.entity_name: self.mapping[self.entity_name]}
#         else:
#             entities_to_process = self.mapping
#
#         print("--- entities_to_process", entities_to_process)
#
#         service = self.get_client()
#
#         for entity_name, timestamp_field in entities_to_process.items():
#             print(f"--- --- processing entity: {entity_name}")
#
#             # get the last modification timestamp (biggest from the Entity's table)
#             model = getattr(bright_models, entity_name)
#             last_updated_record = model.objects.order_by("-" + timestamp_field).first()
#
#             if not last_updated_record:
#                 print(
#                     f"--- --- WARNING! No records found for {entity_name}, starting from the beginning..."
#                 )
#
#             last_update = (
#                 getattr(last_updated_record, timestamp_field)
#                 if last_updated_record
#                 else None
#             )
#             last_update_iso = (
#                 last_update.isoformat(sep="T")
#                 if last_update
#                 else "1970-01-01T00:00:00Z"
#             )
#
#             print(f"--- --- last_update: {last_update_iso}")
#             return
#
#             entity_resource = service.entities[entity_name]
#
#             # make a specific API query to get the entities with the modification timestamp bigger than the last one
#             # TODO add pagination
#             query = (
#                 service.query(entity_resource)
#                 .filter(f"{timestamp_field} gt {last_update_iso}")
#                 .order_by(timestamp_field)
#                 .limit(self.limit)
#             )
#
#             entities = query.all()
#             print(f"--- --- fetched entities: {len(entities)}")
#
#             # self.bulk_update_or_create(model, entities)
#
#             instances = []
#             for entity in entities:
#                 print(
#                     "--- --- --- entity timestamp_field",
#                     entity.__dict__["__odata__"][timestamp_field],
#                 )
#                 instances.append(model.from_python_odata(entity))
#
#             # we need a list of fields of the model
#             fields_to_update = []
#             primary_key_field = None
#             for field in model._meta.get_fields():
#                 if field.primary_key:
#                     primary_key_field = field.name
#                 else:
#                     fields_to_update.append(field.name)
#
#             print("--- --- primary_key_field", primary_key_field)
#
#             # make a bulk create or update operation
#             model.objects.bulk_update_or_create(
#                 instances,
#                 fields_to_update,
#                 match_field=primary_key_field,
#                 batch_size=1000,
#             )
#             print("--- --- saved")
#
#     def bulk_update_or_create(self, model_class, entities_block):
#         """
#         Custom bulk update or create method for the model class
#         """
#         # get model primary key field name
#         primary_key_field = model_class._meta.pk.name
#         print("--- --- primary_key_field", primary_key_field)
#
#         fields_to_update = [
#             field.name
#             for field in model_class._meta.get_fields()
#             if not field.primary_key
#         ]
#         print("--- --- fields_to_update", fields_to_update)
#
#         primary_key_values = []
#
#         for entity in entities_block:
#             # get the primary key value
#             primary_key_values.append(getattr(entity, primary_key_field))
#
#         # get the model instances with the primary key values
#         instances_to_update_queryset = model_class.objects.filter(
#             **{f"{primary_key_field}__in": primary_key_values}
#         )
#         existing_primary_key_values = [
#             getattr(instance, primary_key_field)
#             for instance in instances_to_update_queryset
#         ]
#         print("--- --- existing_primary_key_values", existing_primary_key_values)
#         instances_to_update_dict = {
#             getattr(instance, primary_key_field): instance
#             for instance in instances_to_update_queryset
#         }
#
#         # split entities into two lists: to update and to create
#         instances_to_update = []
#         instances_to_create = []
#         for entity in entities_block:
#             primary_key_value = getattr(entity, primary_key_field)
#             print("--- --- --- primary_key_value", primary_key_value)
#             print(
#                 "--- --- --- entity timestamp_field",
#                 entity.__dict__["__odata__"]["ModificationTimestamp"],
#             )
#
#             if primary_key_value in existing_primary_key_values:
#                 # update the model instance
#                 model_instance = instances_to_update_dict[primary_key_value]
#                 model_instance.update_from_odata(entity)
#                 print(
#                     "--- --- --- model.instance.ModificationTimestamp",
#                     model_instance.ModificationTimestamp,
#                 )
#                 model_instance.save()
#                 instances_to_update.append(model_instance)
#             else:
#                 instances_to_create.append(model_class.from_python_odata(entity))
#
#         print("--- --- instances_to_update", len(instances_to_update))
#         print("--- --- instances_to_update", instances_to_update)
#         print("--- --- instances_to_create", len(instances_to_create))
#         print("--- --- instances_to_create", instances_to_create)
#
#         # if instances_to_update:
#         #     # bulk update the instances
#         #     model_class.objects.bulk_update(
#         #         instances_to_update, fields_to_update, batch_size=500
#         #     )
#
#         if instances_to_create:
#             # bulk create the instances
#             model_class.objects.bulk_create(instances_to_create, batch_size=500)


class BrightMLSUpdateService(BrightMLSBaseService):
    last_update_default = datetime.datetime(
        2024, 11, 1, 0, 0, 0, tzinfo=datetime.timezone.utc
    )

    def update(self):
        last_update = self._get_newest_history_datetime()
        print("--- last_update fetched", last_update)

        # If the last update is lower than specific date, set it to specific date
        if not last_update or last_update < self.last_update_default:
            last_update = self.last_update_default
        print("--- last_update resulted", last_update)

        for entities_block in self._history_entities_iterator(last_update):
            print(f"--- --- fetched entities_block: {len(entities_block)}")
            history_instances = []
            for entity in entities_block:
                # print(
                #     f"--- --- --- entity.PropHistChangeTimestamp: {entity.PropHistChangeTimestamp}"
                # )
                if entity.PropHistTableName == "LISTINGS":
                    if entity.PropHistChangeType == "NEW":
                        self._listing_create(entity)
                    elif entity.PropHistChangeType == "PRICE":
                        self._listing_update_price(entity)
                    elif entity.PropHistChangeType == "STATUS":
                        self._listing_update_status(entity)
                    else:
                        print(
                            f"--- --- --- skipping {entity.PropHistChangeType} action from time {entity.PropHistChangeTimestamp}"
                        )

                history_instances.append(
                    bright_models.History.from_python_odata(entity)
                )

            # bright_models.History.objects.bulk_create(
            #     history_instances, batch_size=1000, ignore_conflicts=True
            # )

    def _get_newest_history_datetime(self):
        record = bright_models.History.objects.first()
        if not record:
            return None

        return record.PropHistChangeTimestamp

    def _history_entities_iterator(self, gt_than_datetime: datetime.datetime):
        service = self.get_client()

        entity_resource = service.entities["History"]

        while True:
            if self.offset >= self.stop:
                print(f"--- --- stopped by STOP arg: {self.stop}")
                break

            print(f"\n--- --- offset:{self.offset}")
            query = (
                service.query(entity_resource)
                .filter(
                    "PropHistChangeTimestamp gt {0}".format(
                        gt_than_datetime.isoformat(sep="T")
                    )
                )
                .order_by("PropHistChangeTimestamp")
            )
            query = query.offset(self.offset).limit(self.limit)

            entities = query.all()
            print(f"--- --- fetched entities: {len(entities)}")

            if not entities:
                print(f"--- --- stopped by entities end")
                break

            self.offset += self.limit

            yield entities

    def _listing_create(self, entity):
        print("--- --- --- --- creating NEW listing", entity.PropHistListingKey)
        # property_entity = (
        #     self.get_client().entities["BrightProperties"].get(listing_key)
        # )
        # print(f"--- --- --- --- exists: {property_entity}")
        # obj = bright_models.BrightProperties.from_python_odata(property_entity)
        # obj.save()

    def _listing_update_price(self, entity):
        print(
            f"--- --- --- --- updating listing PRICE "
            f"for #{entity.PropHistListingKey}, "
            f"column: {entity.PropHistColumnName}, "
            f"from: {entity.PropHistOriginalColumnValue}, to: {entity.PropHistNewColumnValue}"
        )

    def _listing_update_status(self, entity):
        print(
            f"--- --- --- --- updating listing STATUS "
            f"for #{entity.PropHistListingKey}, "
            f"column: {entity.PropHistColumnName}, "
            f"from: {entity.PropHistOriginalColumnValue}, to: {entity.PropHistNewColumnValue}"
        )
