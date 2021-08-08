from flask import Flask

import monitorinsolvenci.config
import monitorinsolvenci.extensions


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    monitorinsolvenci.extensions.db.init_app(app)
    monitorinsolvenci.extensions.migrate.init_app(app, monitorinsolvenci.extensions.db)
    monitorinsolvenci.extensions.login_manager.init_app(app)
    monitorinsolvenci.extensions.login_manager.login_view = 'users.login'
    monitorinsolvenci.extensions.mail.init_app(app)

    from monitorinsolvenci.core.views import core
    from monitorinsolvenci.users.views import users
    from monitorinsolvenci.partners.views import partners
    from monitorinsolvenci.insolvency.views import insolvencies
    from monitorinsolvenci.api.v1 import api as api_v1
    from monitorinsolvenci.error_pages.handlers import error_pages

    app.register_blueprint(core)
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(partners, url_prefix='/partners')
    app.register_blueprint(insolvencies, url_prefix='/insolvencies')
    app.register_blueprint(api_v1, url_prefix='/api/v1')
    app.register_blueprint(error_pages)

    return app
