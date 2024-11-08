from django.core.management.base import BaseCommand, CommandError
from brightmls.services.update import BrightMLSUpdateService


class Command(BaseCommand):
    help = (
        "Command to update the MLS data based on latest historical data from BrightMLS."
    )

    def add_arguments(self, parser):
        # optional string name of the entity argument (will update all entities if not provided)
        parser.add_argument("entity", nargs="?", type=str, help="Entity name")

        # add optional int limit argument
        parser.add_argument(
            "limit",
            nargs="?",
            type=int,
            help="Select count of records to update for each entity",
        )

        # add optional int offset argument
        # parser.add_argument(
        #     "offset",
        #     nargs="?",
        #     type=int,
        #     help="Start the process from this record number",
        # )

        # add optional int stop argument with description
        # parser.add_argument(
        #     "stop",
        #     nargs="?",
        #     type=int,
        #     help="Stop the process at this record number",
        # )

    def handle(self, *args, **options):
        # try:
        service = BrightMLSUpdateService()

        if options["entity"]:
            service.entity_name = options["entity"]
        if options["limit"]:
            service.limit = options["limit"]
        # if options["offset"]:
        #     service.offset = options["offset"]
        # if options["stop"]:
        #     service.stop = options["stop"]

        try:
            service.update()
        except Exception as e:
            raise
            # raise CommandError("Error happens: %s" % e)
        else:
            self.stdout.write(self.style.SUCCESS("Successfully finished"))
