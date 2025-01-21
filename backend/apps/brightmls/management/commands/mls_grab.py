from django.core.management.base import BaseCommand, CommandError

from brightmls.services.grab_linear import BrightMLSGrabService


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

        # add optional int last processed pk argument
        parser.add_argument(
            "last_pk",
            nargs="?",
            type=int,
            help="Start the process from the next record after this one",
        )

    def handle(self, *args, **options):
        service = BrightMLSGrabService()

        service.entity_name = options["entity"][0]
        if options["limit"]:
            service.limit = options["limit"]
        if options["last_pk"]:
            service.last_pk = options["last_pk"]

        try:
            service.populate()
        except Exception as e:
            raise
            # raise CommandError("Error happens: %s" % e)
        else:
            self.stdout.write(self.style.SUCCESS("Successfully finished"))
