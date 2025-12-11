from django.apps import AppConfig


class ProjectApisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'STUDENT_STAGE_APIs'

    def ready(self):
        from . import signals

