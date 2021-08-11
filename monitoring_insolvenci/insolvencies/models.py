import datetime

from monitoring_insolvenci.extensions import db


class Insolvency(db.Model):
    __tablename__ = 'insolvencies'
    id = db.Column(db.Integer, primary_key=True)
    ico = db.Column(db.String(8), index=True)
    case = db.Column(db.String(10), index=True)
    year = db.Column(db.Integer)
    senate_number = db.Column(db.Integer)
    ordering_org = db.Column(db.String(100))
    state = db.Column(db.String(40), index=True)
    url = db.Column(db.String(128))
    bankruptcy_start = db.Column(db.DateTime)
    bankruptcy_end = db.Column(db.DateTime)
    claimed = db.Column(db.Boolean, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    modified = db.Column(db.DateTime, nullable=False)

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
        self.claimed = False
        self.created = datetime.datetime.now()
        self.modified = datetime.datetime.now()

    def update_insolvency(self, new_insolvency_data):
        modified = False
        if self.senate_number is not new_insolvency_data['cisloSenatu']:
            self.senate_number = new_insolvency_data['cisloSenatu']
            modified = True
        if self.ordering_org is not new_insolvency_data['nazevOrganizace']:
            self.ordering_org = new_insolvency_data['nazevOrganizace']
            modified = True
        if self.state is not new_insolvency_data['druhStavKonkursu']:
            self.state = new_insolvency_data['druhStavKonkursu']
            modified = True
        if self.url is not new_insolvency_data['urlDetailRizeni']:
            self.url = new_insolvency_data['urlDetailRizeni']
            modified = True
        if self.bankruptcy_start is not new_insolvency_data['datumPmZahajeniUpadku']:
            self.bankruptcy_start = new_insolvency_data['datumPmZahajeniUpadku']
            modified = True
        if self.bankruptcy_end is not new_insolvency_data['datumPmUkonceniUpadku']:
            self.bankruptcy_end = new_insolvency_data['datumPmUkonceniUpadku']
            modified = True
        if modified:
            self.modified = datetime.datetime.now()

    def to_dict(self):
        if self.bankruptcy_end is not None:
            self.bankruptcy_end = self.bankruptcy_end.strftime("%d.%m.%Y")
        return {
            'id': self.id,
            'ico': self.ico,
            'case': "{}/{}".format(self.case, self.year),
            'senate_number': self.senate_number,
            'ordering_org': self.ordering_org,
            'state': self.state,
            'url': self.url,
            'bankruptcy_start': self.bankruptcy_start.strftime("%d.%m.%Y"),
            'bankruptcy_end': self.bankruptcy_end,
            'claimed': self.claimed,
            'created': self.created,
            'modified': self.modified,
        }
