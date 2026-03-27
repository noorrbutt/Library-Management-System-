import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "librarymanagement.settings")

# Run migrations automatically on Vercel cold start
from django.core.management import call_command

try:
    call_command("migrate", "--run-syncdb", verbosity=0)
except Exception as e:
    print(f"Migration error: {e}")

application = get_wsgi_application()
