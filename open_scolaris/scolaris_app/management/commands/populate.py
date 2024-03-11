from django.core.management.base import BaseCommand, CommandError
from accounts.models import User
import random, sys
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Populate the db with test objects"

    def handle(self, *args, **options):
        roles = ("S", "T", "A")
        users = [
            ("oliviergiroud", "oliviergiroud", "Olivier", "Giroud"),
            ("ousmanedembele", "ousmanedembele", "Ousmane", "Dembélé"),
            ("antoinegriezmann", "antoinegriezmann", "Antoine", "Griezmann"),
            ("kylianmbappe", "kylianmbappe", "Kylian", "Mbappé"),
            ("antoinedupont", "antoinedupont", "Antoine", "Dupont"),
        ]
        for username, password, first_name, last_name in users:
            sys.stdout.write(f"Creating user {username}\n")
            user = get_user_model().objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=random.choice(roles),
            )
            user.save()
