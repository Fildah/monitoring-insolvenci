import datetime

from flask import url_for

from monitoring_insolvenci.extensions import db

partner2insolvency = db.Table('partner2insolvency', db.Column('id', db.Integer, primary_key=True),
                              db.Column('partner_id', db.Integer, db.ForeignKey('partners.id')),
                              db.Column('insolvency_id', db.Integer, db.ForeignKey('insolvencies.id'))
                              )


class Partner(db.Model):
    __tablename__ = 'partners'
    id = db.Column(db.Integer, primary_key=True)
    ico = db.Column(db.String(8), unique=True, index=True)
    dic = db.Column(db.String(20))
    name = db.Column(db.String(128), index=True)
    state = db.Column(db.String(30))
    business_start = db.Column(db.DateTime)
    business_end = db.Column(db.DateTime)
    business_form = db.Column(db.String(50))
    street = db.Column(db.String(128))
    street_number = db.Column(db.String(6))
    orientation_number = db.Column(db.String(6))
    city_part = db.Column(db.String(128))
    city = db.Column(db.String(128))
    zip_code = db.Column(db.String(5))
    country = db.Column(db.String(128))
    created = db.Column(db.DateTime, nullable=False)
    modified = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, default=True)
    insolvencies = db.relationship('Insolvency', secondary=partner2insolvency, backref=db.backref('partner'),
                                   lazy='dynamic')

    def __init__(self, ico, dic, name, state, business_start, business_end, business_form, street, street_number,
                 orientation_number,
                 city_part, city, zip_code, country):
        self.ico = ico
        self.dic = dic
        self.name = name
        self.state = state
        self.business_start = business_start
        self.business_end = business_end
        self.business_form = business_form
        self.street = street
        self.street_number = street_number
        self.orientation_number = orientation_number
        self.city_part = city_part
        self.city = city
        self.zip_code = zip_code
        self.country = country
        self.created = datetime.datetime.now()
        self.modified = datetime.datetime.now()
        self.active = True

    def to_dict(self):
        if self.business_end is not None:
            business_end = self.business_end.strftime("%d.%m.%Y")
        else:
            business_end = "Ne"
        insolvency_count = 0
        insolvency_last_start = "Bez insolvence"
        insolvency_last_end = "Bez insolvence"
        insolvency_last_state = "Bez insolvence"
        if self.insolvencies.count() != 0:
            for insolvency in self.insolvencies:
                if insolvency_count == 0:
                    insolvency_last_start = insolvency.bankruptcy_start
                    insolvency_last_state = insolvency.state
                    if insolvency.bankruptcy_end is not None:
                        insolvency_last_end = insolvency.bankruptcy_end
                else:
                    if insolvency_last_start < insolvency.bankruptcy_start:
                        insolvency_last_start = insolvency.bankruptcy_start
                        insolvency_last_state = insolvency.state
                    if insolvency.bankruptcy_end < insolvency.bankruptcy_end:
                        insolvency_last_end = insolvency.bankruptcy_end
                insolvency_count += 1
            insolvency_last_start = insolvency_last_start.strftime("%d.%m.%Y")
            insolvency_last_end = insolvency_last_end.strftime("%d.%m.%Y")

        if self.street:
            street_address = "{} {}".format(self.street, self.street_number)
        else:
            street_address = "{} {}".format(self.city, self.street_number)
        if self.orientation_number:
            street_address = street_address + "/{}".format(self.orientation_number)
        return {
            'id': self.id,
            'ico': self.ico,
            'dic': self.dic,
            'name': self.name,
            'state': self.state,
            'business_start': self.business_start.strftime("%d.%m.%Y"),
            'business_end': business_end,
            'business_form': self.business_form,
            'street_address': street_address,
            'city_part': self.city_part,
            'city': self.city,
            'zip_code': self.zip_code,
            'country': self.country,
            'del_link': url_for('partners.delete_partner', partner_id=self.id),
            'insolvency_count': insolvency_count,
            'insolvency_last_start': insolvency_last_start,
            'insolvency_last_end': insolvency_last_end,
            'insolvency_last_state': insolvency_last_state,
            'created': self.created,
            'modified': self.modified
        }

    def toggle_active(self):
        self.active = not self.active
        db.session.commit()

    def remove_user(self, user):
        self.users.remove(user)
        db.session.commit()
