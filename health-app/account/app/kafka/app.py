from faust import App

from app.core.settings import settings

app = App('health-app-accounts', broker=settings.KAFKA_BROKER)
