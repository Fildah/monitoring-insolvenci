from flask import Flask

import monitoring_insolvenci.config
import monitoring_insolvenci.extensions


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    monitoring_insolvenci.extensions.db.init_app(app)
    monitoring_insolvenci.extensions.migrate.init_app(app, monitoring_insolvenci.extensions.db)
    monitoring_insolvenci.extensions.login_manager.init_app(app)
    monitoring_insolvenci.extensions.login_manager.login_view = 'users.login'
    monitoring_insolvenci.extensions.mail.init_app(app)

    from monitoring_insolvenci.core.views import core
    from monitoring_insolvenci.users.views import users
    from monitoring_insolvenci.partners.views import partners
    from monitoring_insolvenci.insolvencies.views import insolvencies
    from monitoring_insolvenci.api.v1 import api as api_v1
    from monitoring_insolvenci.error_pages.handlers import error_pages

    app.register_blueprint(core)
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(partners, url_prefix='/partners')
    app.register_blueprint(insolvencies, url_prefix='/insolvencies')
    app.register_blueprint(api_v1, url_prefix='/api/v1')
    app.register_blueprint(error_pages)

    return app
