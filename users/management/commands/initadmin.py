from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Initializing user with role superuser'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(username='admin', email='empty88@gmail.com', password='admin')
            admin.is_admin = True
            admin.is_active = True
            admin.save()