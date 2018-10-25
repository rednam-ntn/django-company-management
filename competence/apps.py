from django.apps import AppConfig


class CompetenceConfig(AppConfig):
    name = 'competence'

    def ready(self):
        import competence.signals  # noqa
