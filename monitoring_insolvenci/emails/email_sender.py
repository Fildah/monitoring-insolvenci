from threading import Thread

from flask import current_app, render_template
from flask_mail import Message

from monitoring_insolvenci import config
from monitoring_insolvenci.extensions import mail


# Odesila email
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


# Pripravuje email k odeslani v ramci dalsiho vlakna
def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(subject, sender=config.MAIL_DEFAULT_SENDER, recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
