import os
import django


def setup_django() -> None:
    """
    Bootstraps Django so this FastAPI service can use the existing Django ORM.
    Update DJANGO_SETTINGS_MODULE if your project name is different.
    """
    #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "khel_ai_mvp.settings")
    django.setup()