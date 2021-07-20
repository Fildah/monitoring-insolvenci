from sledovacinsolvenci.extensions import db

subscribers = db.Table('subscribers', db.Column('id', db.Integer, primary_key=True),
                       db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                       db.Column('partner_id', db.Integer, db.ForeignKey('partners.id'))
                       )


class Partner(db.Model):
    __tablename__ = 'partners'
    id = db.Column(db.Integer, primary_key=True)
    ico = db.Column(db.String(8), unique=True, index=True)
    dic = db.Column(db.String(20))
    name = db.Column(db.String(128), index=True)
    state = db.Column(db.String(30))
    created = db.Column(db.Date)
    closed = db.Column(db.Date)
    business_form = db.Column(db.String(50))
    street = db.Column(db.String(128))
    street_number = db.Column(db.String(6))
    orientation_number = db.Column(db.String(6))
    city_part = db.Column(db.String(128))
    city = db.Column(db.String(128))
    zip_code = db.Column(db.String(5))
    country = db.Column(db.String(128))
    active = db.Column(db.Boolean, default=True)

    def __init__(self, ico, dic, name, state, created, closed, business_form, street, street_number, orientation_number,
                 city_part, city, zip_code, country):
        self.ico = ico
        self.dic = dic
        self.name = name
        self.state = state
        self.created = created
        self.closed = closed
        self.business_form = business_form
        self.street = street
        self.street_number = street_number
        self.orientation_number = orientation_number
        self.city_part = city_part
        self.city = city
        self.zip_code = zip_code
        self.country = country
        self.active = True

    def to_dict(self):
        return {
            'ico': self.ico,
            'dic': self.dic,
            'name': self.name,
            'business_form': self.business_form,
            'state': self.state,
            'street': self.street,
            'street_number': self.street_number,
            'orientation_number': self.orientation_number,
            'city_part': self.city_part,
            'city': self.city,
            'zip_code': self.zip_code,
            'country': self.country
        }
