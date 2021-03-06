# fmt: off
import sentry_sdk
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sentry_sdk.integrations.flask import FlaskIntegration

from backend.application.settings import BackendSettings

sentry_sdk.init(dsn=BackendSettings.SENTRY_DNS, integrations=[FlaskIntegration()])

backend_application = Flask(
    import_name=__name__,
    static_url_path="/static/",
    static_folder=f"{BackendSettings.BASE_DIR}/static",
    template_folder=f"{BackendSettings.BASE_DIR}/frontend"
)
backend_application.config.from_object(BackendSettings)
db = SQLAlchemy(backend_application)

from backend import models  # noqa
from backend import routes  # noqa
from backend import scheduler  # noqa
# fmt: on
