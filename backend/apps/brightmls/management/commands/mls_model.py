from django.core.management.base import BaseCommand, CommandError
from brightmls.services import BrightMLSService


class Command(BaseCommand):
    help = "Command to generate the model from the MLS metadata"

    def add_arguments(self, parser):
        parser.add_argument("entity", nargs=1, type=str, help="Entity name")

    def handle(self, *args, **options):
        # try:
        service = BrightMLSService()

        try:
            service.populate()
        except Exception as e:
            raise
            # raise CommandError("Error happens: %s" % e)
        else:
            self.stdout.write(self.style.SUCCESS("Successfully finished"))
