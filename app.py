import config

from flask import Flask

from internwatch.models import db
from internwatch.views import register_routes

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
register_routes(app)

