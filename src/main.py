from flask import Flask
from config.settings import settings
from api.routes import api_blueprint
from config.logging_config import get_logger

logger = get_logger(__name__)

def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(api_blueprint)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        host=settings.flask_api.HOST,
        port=settings.flask_api.PORT,
        debug=settings.flask_api.DEBUG
    )