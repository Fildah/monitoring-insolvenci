import datetime

from monitoring_insolvenci.extensions import db


# Trida User pro ukladani insolvenci
class Insolvency(db.Model):
    # Parametry tabulky
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

    # Inicializace tridy
    # Prijima string ico, case, ordering_org, state, url & int year, senate_number
    # & datetime bankruptcy_start, bankruptcy_end
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

    # Updatuje insolvenci
    # Prijima slovnik s novymi udaji o insolvenci
    # Vraci slovnik se zmenami nebo False
    def update_insolvency(self, new_insolvency_data):
        update = {'changed': False, 'old_data': {}}
        if self.senate_number != new_insolvency_data['cisloSenatu']:
            update['old_data']['senate_number'] = self.senate_number
            update['changed'] = True
            self.senate_number = new_insolvency_data['cisloSenatu']
        if self.ordering_org != new_insolvency_data['nazevOrganizace']:
            update['old_data']['ordering_org'] = self.ordering_org
            update['changed'] = True
            self.ordering_org = new_insolvency_data['nazevOrganizace']
        if self.state != new_insolvency_data['druhStavKonkursu']:
            update['old_data']['state'] = self.state
            update['changed'] = True
            self.state = new_insolvency_data['druhStavKonkursu']
        if self.bankruptcy_start != new_insolvency_data['datumPmZahajeniUpadku']:
            update['old_data']['bankruptcy_start'] = self.bankruptcy_start.strftime("%d.%m.%Y")
            update['changed'] = True
            self.bankruptcy_start = new_insolvency_data['datumPmZahajeniUpadku']
        if self.bankruptcy_end != new_insolvency_data['datumPmUkonceniUpadku']:
            update['old_data']['bankruptcy_end'] = self.bankruptcy_end.strftime("%d.%m.%Y")
            update['changed'] = True
            self.bankruptcy_end = new_insolvency_data['datumPmUkonceniUpadku']
        if update['changed']:
            self.modified = datetime.datetime.now()
            update.pop('changed')
            update['new_data'] = self.to_dict()
            update['time'] = self.modified
            update['type'] = 'update'
            return update
        else:
            return False

    # Generuje slovnik z atributu instance Insolvency
    # Vraci slovnik s udaji Insolvency
    def to_dict(self):
        if self.bankruptcy_end is not None:
            bankruptcy_end = self.bankruptcy_end.strftime("%d.%m.%Y")
        return {
            'id': self.id,
            'ico': self.ico,
            'case': "{}/{}".format(self.case, self.year),
            'senate_number': self.senate_number,
            'ordering_org': self.ordering_org,
            'state': self.state,
            'url': self.url,
            'bankruptcy_start': self.bankruptcy_start.strftime("%d.%m.%Y"),
            'bankruptcy_end': bankruptcy_end,
            'claimed': self.claimed,
            'created': self.created,
            'modified': self.modified,
        }
