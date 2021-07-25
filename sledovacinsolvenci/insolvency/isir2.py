import certifi
from requests import Session
from zeep import Client, Settings
from zeep.helpers import serialize_object
from zeep.transports import Transport

from sledovacinsolvenci.insolvency.models import Insolvency


def fill_insolvency_with_isir(insolvency_data):
    return Insolvency(
        ico=insolvency_data['ic'],
        case=insolvency_data['bcVec'],
        year=insolvency_data['rocnik'],
        senate_number=insolvency_data['cisloSenatu'],
        ordering_org=insolvency_data['nazevOrganizace'],
        state=insolvency_data['druhStavKonkursu'],
        url=insolvency_data['urlDetailRizeni'],
        bankruptcy_start=insolvency_data['datumPmZahajeniUpadku'],
        bankruptcy_end=insolvency_data['datumPmUkonceniUpadku']
    )


class Isir:
    def __init__(self):
        session = Session()
        session.verify = certifi.where()
        transport = Transport(session=session)
        settings = Settings(strict=False)
        self.client = Client(wsdl='https://isir.justice.cz:8443/isir_cuzk_ws/IsirWsCuzkService?wsdl',
                             transport=transport, settings=settings)

    def get_ico_insolvencies(self, ico):
        ico_insolvencies = list()
        try:
            all_insolvencies = serialize_object(self.client.service.getIsirWsCuzkData(ic=ico))
        except:
            return None
        for insolvency in all_insolvencies['data']:
            if insolvency['ic'] != ico:
                continue
            ico_insolvencies.append(insolvency)
        return ico_insolvencies
