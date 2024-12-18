from django.core.management.base import BaseCommand, CommandError
from brightmls.services.grab_linear import BrightMLSGrabService
from brightmls.services.grab_threaded import BrightMLSGrabThreadedService


class Command(BaseCommand):
    help = "Command to populate the database from the zero state"

    def add_arguments(self, parser):
        # mandatory string name of the entity argument
        parser.add_argument(
            "entity", nargs=1, type=str, help="Entity name (the same as Model name)"
        )

        # add optional int limit argument
        parser.add_argument(
            "limit",
            nargs="?",
            type=int,
            help="Select this count of records once (defaults to 10000)",
        )

        # add optional int offset argument
        parser.add_argument(
            "offset",
            nargs="?",
            type=int,
            help="Start the process from this record number (defaults to 0)",
        )

        # add optional int stop argument with description
        parser.add_argument(
            "stop",
            nargs="?",
            type=int,
            help="Stop the process at this record number (defaults to the end of the table)",
        )

    def handle(self, *args, **options):
        service = BrightMLSGrabThreadedService()

        service.entity_name = options["entity"][0]
        if options["limit"]:
            service.limit = options["limit"]
        if options["offset"]:
            service.offset = options["offset"]
        if options["stop"]:
            service.stop = options["stop"]

        try:
            service.populate()
        except Exception as e:
            raise
            # raise CommandError("Error happens: %s" % e)
        else:
            self.stdout.write(self.style.SUCCESS("Successfully finished"))
