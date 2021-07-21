import certifi
from requests import Session
from zeep import Client, Settings
from zeep.transports import Transport


class Isir:
    def __init__(self, wsdl):
        session = Session()
        session.verify = certifi.where()
        transport = Transport(session=session)
        settings = Settings(strict=False)
        self.client = Client(wsdl=wsdl, transport=transport, settings=settings)

    def get_isir_data(self, ico):
        return self.client.service.getIsirWsCuzkData(ic=ico)
