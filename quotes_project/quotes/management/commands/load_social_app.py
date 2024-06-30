import json
from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

class Command(BaseCommand):
    help = 'Load social app configuration from JSON file'

    def handle(self, *args, **options):
        with open('social_app_config.json') as f:
            config = json.load(f)

        site = Site.objects.get(id=config["sites"][0])

        app, created = SocialApp.objects.get_or_create(
            provider=config["provider"],
            name=config["name"]
        )
        app.client_id = config["client_id"]
        app.secret = config["secret"]
        app.save()
        app.sites.set([site])

        if created:
            self.stdout.write(self.style.SUCCESS('Social app created successfully.'))
        else:
            self.stdout.write(self.style.SUCCESS('Social app updated successfully.'))
