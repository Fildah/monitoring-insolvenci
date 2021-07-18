from sledovacinsolvenci.extensions import db

subscribers = db.Table('subscribers', db.Column('id', db.Integer, primary_key=True),
                       db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                       db.Column('partner_id', db.Integer, db.ForeignKey('partners.id'))
                       )


class Partner(db.Model):
    __tablename__ = 'partners'
    id = db.Column(db.Integer, primary_key=True)
    ico = db.Column(db.String(8), unique=True, index=True)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, ico):
        self.ico = ico
        self.active = True
