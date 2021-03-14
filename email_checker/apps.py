from django.apps import AppConfig


class EmailCheckerConfig(AppConfig):
    name = 'email_checker'

    def ready(self):
        import email_checker.signals  # noqa
