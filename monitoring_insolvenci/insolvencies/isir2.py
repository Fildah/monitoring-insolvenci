import certifi
from requests import Session
from zeep import Client, Settings
from zeep.helpers import serialize_object
from zeep.transports import Transport

from monitoring_insolvenci.insolvencies.models import Insolvency


# Vytvari novou Insolvency z udaju z ISIRu
# Prijima slovnik udaju z ISIRu
# Vraci instanci Insolvency
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


# Trida Isir pro moznost volani sluzby ISIR
class Isir:
    # Inicializace tridy
    def __init__(self):
        session = Session()
        session.verify = certifi.where()
        transport = Transport(session=session)
        settings = Settings(strict=False)
        self.client = Client(wsdl='https://isir.justice.cz:8443/isir_cuzk_ws/IsirWsCuzkService?wsdl',
                             transport=transport, settings=settings)

    # Ziskava data o ICO z ISIR
    # Prijima int ico
    # Vraci slovnik s udaji z ISIR nebo False
    def get_ico_insolvencies(self, ico):
        ico_insolvencies = list()
        try:
            all_insolvencies = serialize_object(self.client.service.getIsirWsCuzkData(ic=ico))
        except:
            return False
        for insolvency in all_insolvencies['data']:
            if insolvency['ic'] != ico:
                continue
            ico_insolvencies.append(insolvency)
        if len(ico_insolvencies) == 0:
            return False
        else:
            return ico_insolvencies
