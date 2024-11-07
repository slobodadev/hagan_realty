import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from brightmls import models as bright_models
from brightmls.services.base import BrightMLSBaseService

logger = logging.getLogger("brightmls.services")


class BrightMLSGrabThreadedService(BrightMLSBaseService):
    def populate(self):
        """
        Populate data from the API in a threaded manner from `offset` to `stop`.
        If `stop` is None, continue until no more entities are available.
        """
        start_timestamp = datetime.now()

        if not self.entity_name:
            raise ValueError("Entity name must be set before calling populate.")

        model_class = getattr(bright_models, self.entity_name)

        # clear the table before populating if truncate_table is set
        # model_class.objects.all().delete()

        current_offset = self.offset

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            while True:
                if self.stop and current_offset >= self.stop:
                    logger.debug(
                        f"reached stop={self.stop} by current_offset={current_offset}"
                    )
                    break

                futures = {}
                for offset in range(
                    current_offset,
                    current_offset + self.limit * self.max_workers,
                    self.limit,
                ):
                    if not self.stop or offset < self.stop:
                        # to prevent grab more than stop
                        limit = self.limit
                        if self.stop and offset + self.limit > self.stop:
                            limit = self.stop - offset

                        future = executor.submit(
                            self._grab_and_save, model_class, limit, offset
                        )
                        futures[future] = offset

                last_offset = offset

                # logging.debug(f"--- futures: {futures}")

                # Move to the next batch
                current_offset += self.limit * self.max_workers

                # Process results as they complete
                more_entities = True
                for future in as_completed(futures):
                    offset = futures[future]
                    try:
                        # Fetch result to check if entities were returned
                        result = future.result()
                        # logging.debug(f"--- result: {result} at offset {offset}")
                        # if at least one thread returns no entities, stop the process
                        more_entities &= result
                    except Exception as exc:
                        logging.error(f"Error at offset {offset}: {exc}")
                        return

                # logging.debug(f"--- more_entities: {more_entities}")

                if not more_entities:
                    break  # Stop if no more entities are returned from the API

        end_timestamp = datetime.now()
        logger.info(
            f"Finished populating  {self.entity_name} in {end_timestamp - start_timestamp}, lsat offset: {last_offset}"
        )

    def _grab_and_save(self, model_class, limit: int, offset: int):
        """
        Fetches entities and saves them to the database within each thread.
        Returns True if entities were found, False otherwise.
        """
        # logging.debug(f"--- started iteration offset={offset}, limit={limit}")
        entities = self._entities_grab(limit, offset)
        logging.debug(
            f"--- fetched entities: {len(entities)}, offset={offset}, limit={limit}"
        )
        if entities:
            self._entities_save(model_class, entities)
            return True

        return False

    def _entities_grab(self, limit: int, offset: int):
        service = self.get_client()
        entity_resource = service.entities[self.entity_name]
        query = service.query(entity_resource)
        query = query.offset(offset).limit(limit)
        entities = query.all()
        return entities

    def _entities_save(self, model_class, entities):
        instances = []
        for entity in entities:
            instances.append(model_class.from_python_odata(entity))
        model_class.objects.bulk_create(
            instances, batch_size=500, ignore_conflicts=True
        )
