import datetime

from sledovacinsolvenci.extensions import db

partner2insolvency = db.Table('partner2insolvency', db.Column('id', db.Integer, primary_key=True),
                              db.Column('partner_id', db.Integer, db.ForeignKey('partners.id')),
                              db.Column('insolvency_id', db.Integer, db.ForeignKey('insolvency.id'))
                              )


class Insolvency(db.Model):
    __tablename__ = 'insolvency'
    id = db.Column(db.Integer, primary_key=True)
    ico = db.Column(db.String(8), index=True)
    case = db.Column(db.String(10), index=True)
    year = db.Column(db.Integer)
    senate_number = db.Column(db.Integer)
    ordering_org = db.Column(db.String(100))
    state = db.Column(db.String(40), index=True)
    url = db.Column(db.String(128))
    bankruptcy_start = db.Column(db.Date)
    bankruptcy_end = db.Column(db.Date)
    created = db.Column(db.Date, nullable=False)
    modified = db.Column(db.Date, nullable=False)

    def __init__(self, ico, case, year, senate_number, ordering_org, state, url, bankruptcy_start, bankruptcy_end):
        self.ico = ico
        self.case = case
        self.year = year
        self.senate_number = senate_number
        self.ordering_org = ordering_org
        self.state = state
        self.url = url
        self.bankruptcy_start = bankruptcy_start
        self.bankruptcy_end = bankruptcy_end
        self.created = datetime.datetime.now()
        self.modified = datetime.datetime.now()
