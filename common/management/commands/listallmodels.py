from typing import Any

from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "List all models in all apps with their fields and constraints"

    def handle(self, *args: Any, **options: Any) -> str | None:
        installed_apps = apps.get_app_configs()

        for app in installed_apps:
            models = app.get_models()
            self.stdout.write(f"App: {app.verbose_name}")

            for model in models:
                self.stdout.write(f"  Model: {model._meta.verbose_name}")

                for field in model._meta.get_fields():
                    self.stdout.write(
                        f"    Field: {field.name}, Type: {field.__class__.__name__}"
                    )

                    constraints = (
                        field.constraints if hasattr(field, "constraints") else None
                    )

                    if constraints:
                        self.stdout.write("      Constraints:")
                        for constraint in constraints:
                            self.stdout.write(
                                f"        {constraint.__class__.__name__}"
                            )
