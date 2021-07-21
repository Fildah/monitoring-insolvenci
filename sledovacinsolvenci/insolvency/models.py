from sledovacinsolvenci.extensions import db

partner2insolvency = db.Table('partner2insolvency', db.Column('id', db.Integer, primary_key=True),
                              db.Column('partner_id', db.Integer, db.ForeignKey('partners.id')),
                              db.Column('insolvency_id', db.Integer, db.ForeignKey('insolvency.id'))
                              )


class Insolvency(db.Model):
    __tablename__ = 'insolvency'
    id = db.Column(db.Integer, primary_key=True)
    case = db.Column(db.String(10), index=True)
    year = db.Column(db.Integer)
    state = db.Column(db.String(128), index=True)
    created = db.Column(db.Date, nullable=False)
    modified = db.Column(db.Date, nullable=False)

    def __init__(self, partner_id, case, state, created, modified):
        self.partner_id = partner_id
        self.case = case
        self.state = state
        self.created = created
        self.modified = modified
