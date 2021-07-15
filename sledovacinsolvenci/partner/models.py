from sledovacinsolvenci import db


class Partner(db.Model):
    __tablename__ = 'partners'
    id = db.Column(db.Integer, primary_key=True)
    ico = db.Column(db.String(8), unique=True, index=True)
    insolvence = db.relationship('Insolvence', backref='ucastnik', lazy=True)

    def __init__(self, ico):
        self.ico = ico
