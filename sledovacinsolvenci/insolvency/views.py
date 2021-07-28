from flask import render_template, Blueprint, request
from flask_login import login_required, current_user

from sledovacinsolvenci.extensions import db
from sledovacinsolvenci.insolvency.isir2 import Isir, fill_insolvency_with_isir
from sledovacinsolvenci.insolvency.models import Insolvency
from sledovacinsolvenci.partners.models import Partner

insolvencies = Blueprint('insolvencies', __name__)


@insolvencies.get('/')
@login_required
def user_insolvencies():
    return render_template('user_insolvencies.html', title='Sledované insolvence partnerů', user=current_user)


# TODO Presunout do API
@insolvencies.get('/api', defaults={'partner_id': None})
@insolvencies.get('/api/<int:partner_id>')
@login_required
def api_insolvencies(partner_id):
    if partner_id is not None:
        query = Insolvency.query.filter(Insolvency.partner.any(Partner.id.in_([partner_id])))
    else:
        query = Insolvency.query.filter(Insolvency.partner.any(Partner.users.contains(current_user)))
    all_user_insolvencies = query.count()
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Insolvency.ico.like('%{}%'.format(search)),
            Insolvency.case.like('%{}%'.format(search)),
            Insolvency.state.like('%{}%'.format(search)),
            Insolvency.bankruptcy_start.like('%{}%'.format(search)),
            Insolvency.bankruptcy_end.like('%{}%'.format(search))
        ))
    total_filtered = query.count()
    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['ico', 'state', 'bankruptcy_start', 'bankruptcy_end']:
            col_name = 'name'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(Insolvency, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)
    return {
        'data': [insolvency.to_dict() for insolvency in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': all_user_insolvencies,
        'draw': request.args.get('draw', type=int),
    }


@insolvencies.cli.command()
def update_insolvencies():
    isir = Isir()
    all_partners = Partner.query.all()
    for partner in all_partners:
        insolvencies_for_ico = isir.get_ico_insolvencies(partner.ico)
        for insolvency_data in insolvencies_for_ico:
            existing_insolvency = Insolvency.query.filter_by(ico=partner.ico, case=insolvency_data['bcVec'],
                                                             year=insolvency_data['rocnik']).first()
            if partner.insolvencies is not None:
                if existing_insolvency is None:
                    insolvency = fill_insolvency_with_isir(insolvency_data)
                    insolvency.partner.append(partner)
                    db.session.add(insolvency)
                else:
                    existing_insolvency.update_insolvency(insolvency_data)
        db.session.commit()
