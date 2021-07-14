from sledovacinsolvenci import db


class Partner(db.Model):
    __tablename__ = 'partners'
    id = db.Column(db.Integer, primary_key=True)
    ico = db.Column(db.String(8), unique=True, index=True)
    insolvence = db.relationship('Insolvence', backref='ucastnik', lazy=True)

    def __init__(self, ico):
        self.ico = ico


class Insolvence(db.Model):
    __tablename__ = 'insolvence'
    id = db.Column(db.Integer, primary_key=True)
    partner_id = db.Column(db.Ineger, db.ForeignKey('partners.id'), nullable=False)
    case = db.Column(db.String(10), index=True)
    state = db.Column(db.String(128), index=True)
    created = db.Column(db.Date, nullable=False)
    modified = db.Column(db.Date, nullable=False)

    def __init__(self, partner_id, case, state, created, modified):
        self.partner_id = partner_id
        self.case = case
        self.state = state
        self.created = created
        self.modified = modified
