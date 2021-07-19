import requests

if __name__ == '__main__':
    #  wsdl = 'https://wwwinfo.mfcr.cz/ares/xml_doc/wsdl/standard.wsdl'
    #  session = Session()
    #  session.verify = False
    #  transport = Transport(session=session)
    #  client = Client(wsdl=wsdl, transport=transport)
    #  print(client.service.GetXmlFile(
    #      Dotaz=[{'Pomocne_ID': '1', 'Typ_vyhledani': 'FREE', 'Klicove_polozky': {'ICO': '02633582'}, 'Max_pocet': 10}],
    #      dotaz_datum_cas=datetime.datetime.now().isoformat(), dotaz_pocet=1, dotaz_typ='Basic', vystup_format='XML',
    #      user_mail='test@test.te',
    #      validation_XSLT="https://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_request/v_1.0.1/ares_request_v_1.0.1.xsd",
    #      answerNamespaceRequired='https://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer_basic/v_1.0.2/ares_answer_basic_v_1.0.2.xsd',
    #      Id='ares_dotaz'))
    response = requests.get('http://wwwinfo.mfcr.cz/cgi-bin/ares/xar.cgi', params={'ico': '02633582'})
    print(response.text)
