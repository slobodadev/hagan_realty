from django.core.management.base import BaseCommand, CommandError
from brightmls import models as bright_models


class Command(BaseCommand):
    help = "Command to truncate specific MLS data table"

    def add_arguments(self, parser):
        # optional string name of the entity argument (will update all entities if not provided)
        parser.add_argument(
            "entity", type=str, help="Entity name (The same as Model name)"
        )

    def handle(self, *args, **options):
        try:
            model_class = getattr(bright_models, options["entity"])
        except AttributeError:
            raise CommandError(f"Model {options['entity']} not found")

        model_class.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(f"Successfully truncated {options['entity']} table")
        )
