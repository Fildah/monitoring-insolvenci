import requests
import xmltodict

from monitorinsolvenci.partners.models import Partner


def get_ares_data(ico):
    response = requests.get('https://wwwinfo.mfcr.cz/cgi-bin/ares/darv_bas.cgi?ico={}&aktivni=false'.format(ico))
    response.encoding = 'UTF-8'
    ares = xmltodict.parse(response.text)
    partner_data = dict()
    if 'D:E' not in ares['are:Ares_odpovedi']['are:Odpoved']:
        ares_vbas = ares['are:Ares_odpovedi']['are:Odpoved']['D:VBAS']
        ares_aa = ares_vbas['D:AA']
        partner_data['ico'] = ares_vbas['D:ICO']['#text']
        if 'D:DIC' in ares_vbas:
            partner_data['dic'] = ares_vbas['D:DIC']['#text']
        else:
            partner_data['dic'] = None
        partner_data['name'] = ares_vbas['D:OF']['#text']
        if 'D:ROR' in ares_vbas:
            partner_data['state'] = ares_vbas['D:ROR']['D:SOR']['D:SSU']
        else:
            partner_data['state'] = 'Neaktivní'
        partner_data['business_start'] = ares_vbas['D:DV']
        if 'D:DZ' in ares_vbas:
            partner_data['business_end'] = ares_vbas['D:DZ']
        else:
            partner_data['business_end'] = None
        partner_data['business_form'] = ares_vbas['D:PF']['D:NPF']
        if 'D:NU' in ares_aa:
            partner_data['street'] = ares_aa['D:NU']
        else:
            partner_data['street'] = None
        if 'D:CD' in ares_aa:
            partner_data['street_number'] = ares_aa['D:CD']
        else:
            partner_data['street_number'] = None
        if 'D:CO' in ares_aa:
            partner_data['orientation_number'] = ares_aa['D:CO']
        else:
            partner_data['orientation_number'] = None
        if 'D:NCO' in ares_aa:
            partner_data['city_part'] = ares_aa['D:NCO']
        else:
            partner_data['city_part'] = None
        if 'D:N' in ares_aa:
            partner_data['city'] = ares_aa['D:N']
        else:
            partner_data['city'] = None
        if 'D:PSC' in ares_aa:
            partner_data['zip_code'] = ares_aa['D:PSC']
        else:
            partner_data['zip_code'] = None
        if 'D:NS' in ares_aa:
            partner_data['country'] = ares_aa['D:NS']
        else:
            partner_data['country'] = None
        return partner_data
    return None


def fill_partner_with_ares(partner_ares):
    return Partner(
        ico=partner_ares['ico'],
        dic=partner_ares['dic'],
        name=partner_ares['name'],
        state=partner_ares['state'],
        business_start=partner_ares['business_start'],
        business_end=partner_ares['business_end'],
        business_form=partner_ares['business_form'],
        street=partner_ares['street'],
        street_number=partner_ares['street_number'],
        orientation_number=partner_ares['orientation_number'],
        city_part=partner_ares['city_part'],
        city=partner_ares['city'],
        zip_code=partner_ares['zip_code'],
        country=partner_ares['country']
    )
