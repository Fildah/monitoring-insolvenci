from flask import Flask

import sledovacinsolvenci.config
import sledovacinsolvenci.extensions


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    sledovacinsolvenci.extensions.db.init_app(app)
    sledovacinsolvenci.extensions.migrate.init_app(app, sledovacinsolvenci.extensions.db)
    sledovacinsolvenci.extensions.login_manager.init_app(app)
    sledovacinsolvenci.extensions.login_manager.login_view = 'users.login'

    from sledovacinsolvenci.core.views import core
    from sledovacinsolvenci.users.views import users
    from sledovacinsolvenci.partners.views import partners
    from sledovacinsolvenci.insolvency.views import insolvency
    from sledovacinsolvenci.error_pages.handlers import error_pages

    app.register_blueprint(core)
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(partners, url_prefix='/partners')
    app.register_blueprint(insolvency, url_prefix='/insolvency')
    app.register_blueprint(error_pages)

    return app
