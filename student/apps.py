from django.apps import AppConfig


class StudentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'student'

class YourAppConfig(AppConfig):
    name = 'student'

    def ready(self):
        import student.signals