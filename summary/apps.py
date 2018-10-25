from django.apps import AppConfig


class SummaryConfig(AppConfig):
    name = 'summary'

    def ready(self):
        import summary.signals  # noqa
