import tracemalloc
from datetime import datetime
from brightmls import models as bright_models
from brightmls.services.base import BrightMLSBaseService


class BrightMLSGrabService(BrightMLSBaseService):
    """
    Service to grab data from Bright MLS API and populate the database.
    Uses OData protocol to fetch data in chunks.
    Uses sequential approach to fetch data and NextLink to paginate. Can not be parallelized.
    """

    last_pk = None
    total_inserted = 0
    start_timestamp = None

    def populate(self):
        service = self.get_client()

        print(f">> Grabbing entity: {self.entity_name}")

        try:
            entity_resource = service.entities[self.entity_name]
        except KeyError:
            raise ValueError(
                f"Entity {self.entity_name} not found. "
                f"Provide the name in camel case as it specified on Bright MLS website"
            )

        model_class = getattr(bright_models, self.entity_name)

        tracemalloc.start()
        self.start_timestamp = datetime.now()

        # Try to get the last record if not forced
        if self.last_pk is not None:
            print(f">> starting from the last_pk forced as command arg: {self.last_pk}")
        else:
            self.last_pk = self._get_biggest_pk(model_class)
            if self.last_pk is not None:
                print(f">> starting from the last_pk found in database: {self.last_pk}")

        if self.last_pk is None:
            print(f">> starting from the beginning of dataset")

        query = service.query(entity_resource)

        # set skip token if last pk is provided or exists in the database. Start from the beginning otherwise
        if self.last_pk:
            skip_token = f"last_pk:{self.last_pk},odata.maxpagesize:{self.limit}"
            query.skiptoken(skip_token)

        entities = []
        for entity in query:
            # print(entity.__dict__)
            entities.append(entity)

            if len(entities) >= self.limit:
                self._insert_entities(model_class, entities)
                entities = []

        if entities:
            self._insert_entities(model_class, entities)

    def _insert_entities(self, model_class, entities):
        self._bulk_create_simple(model_class, entities)
        self.total_inserted += len(entities)
        print(".", end="", flush=True)

        if self.total_inserted % (self.limit * 10) == 0:
            # gc.collect()

            # memory usage
            current, peak = tracemalloc.get_traced_memory()
            current_mb = current / 10**6
            peak_mb = peak / 10**6
            tracemalloc.reset_peak()
            memory = f"(mem usage: {current_mb:.1f}MB; peak {peak_mb:.1f}MB)"

            # last inserted pk
            pk_field = self._get_models_pk_name(model_class)
            last_pk = getattr(entities[-1], pk_field)
            last_pk_str = f"(last pk: {last_pk})"

            # time from start
            point_timestamp = datetime.now()
            time_from_start = point_timestamp - self.start_timestamp
            formatted_time = str(time_from_start).split(".")[0]
            time_string = f"(time: {formatted_time})"

            print(
                f"{self.total_inserted:,}", last_pk_str, memory, time_string, flush=True
            )

    def _bulk_create_simple(self, model_class, entities_block):
        instances = []
        for entity in entities_block:
            instances.append(model_class.from_python_odata(entity))

        model_class.objects.bulk_create(
            instances, batch_size=500, ignore_conflicts=True
        )

    def _get_models_pk_name(self, model_class):
        return model_class._meta.pk.name

    def _get_biggest_pk(self, model_class):
        pk_field = self._get_models_pk_name(model_class)
        last_record = model_class.objects.order_by(f"-{pk_field}").first()
        return getattr(last_record, pk_field) if last_record else None
