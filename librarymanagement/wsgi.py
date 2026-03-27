import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "librarymanagement.settings")

from django.core.management import call_command

try:
    call_command("migrate", "--run-syncdb", verbosity=0)

    # Seed the Site object required by django-allauth
    from django.contrib.sites.models import Site
    from django.conf import settings

    Site.objects.update_or_create(
        id=settings.SITE_ID,
        defaults={
            "domain": "library-management-system-snowy-nine.vercel.app",
            "name": "Library Management System",
        },
    )
except Exception as e:
    print(f"Setup error: {e}")

application = get_wsgi_application()
