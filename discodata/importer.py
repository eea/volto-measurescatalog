""" Import data from Discodata
    https://discodata.eea.europa.eu/
    WISE_ShippingsPorts_Measures - latest
"""
#!/usr/bin/env python3

import json
import requests

sql_views = {
    'vw_master_BD_2013_2018':
        'https://discodata.eea.europa.eu/sql?query=' \
        'Select%20*%20from%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.' \
        'vw_master_BD_2013_2018&p=1&nrOfHits=100&mail=null&schema=null',
    'vw_master_HD_Habitats_2013_2018_Filtered':
        'https://discodata.eea.europa.eu/sql?query=' \
        'Select%20*%20from%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.' \
        'vw_master_HD_Habitats_2013_2018_Filtered%0A&p=1&nrOfHits=100&mail=null' \
        '&schema=null',
    'vw_master_HD_Species_2013_2018_Filtered':
        'https://discodata.eea.europa.eu/sql?query=' \
        'Select%20*%20from%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.' \
        'vw_master_HD_Species_2013_2018_Filtered%0A&p=1&nrOfHits=100&mail=null&' \
        'schema=null',
    'vw_master_MSFD_Filtered':
        'https://discodata.eea.europa.eu/sql?query=' \
        'Select%20*%20from%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.'\
        'vw_master_MSFD_Filtered%0A&p=1&nrOfHits=100&mail=null&schema=null',
    'vw_master_MSPD':
        'https://discodata.eea.europa.eu/sql?query=' \
        'Select%20*%20from%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.' \
        'vw_master_MSPD%0A&p=1&nrOfHits=100&mail=null&schema=null',
    'vw_master_Sectorial':
        'https://discodata.eea.europa.eu/sql?query=' \
        'Select%20*%20from%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.' \
        'vw_master_Sectorial%0A&p=1&nrOfHits=100&mail=null&schema=null',
    'vw_master_WFD_Filtered':
        'https://discodata.eea.europa.eu/sql?query=' \
        'Select%20*%20from%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.' \
        'vw_master_WFD_Filtered%0A&p=1&nrOfHits=100&mail=null&schema=null',
    'vw_master':
        'https://discodata.eea.europa.eu/sql?query=' \
        'Select%20*%20from%20%5BWISE_ShippingsPorts_Measures%5D.' \
        '%5Blatest%5D.vw_master%0A&p=1&nrOfHits=100&mail=null&schema=null',
}

fields = {
    'catalogueCode': 'CodeCatalogue',
    'sector': 'Sector',
    'useOrActivity': 'Use or activity',
    'measureName': 'Measure name',
    'status': 'Status',
    'measureOrigin': 'Origin of the measure',
    'measureNature': 'Nature of the measure',
    'waterBodyCategory': 'Water body category',
    'spatialScope': 'Spatial scope',
    'country': 'Country',
    'measureImpactTo': 'Measure Impacts to',
    'measureImpactToDetails': 'Measure Impacts to (further details)',
    'D1': 'D1',
    'D2': 'D2',
    'D3': 'D3',
    'D4': 'D4',
    'D5': 'D5',
    'D6': 'D6',
    'D7': 'D7',
    'D8': 'D8',
    'D9': 'D9',
    'D10': 'D10',
    'D11': 'D11',
    # ? missing id? Example '_id': 'WFD11'
}

def nice_print(data):
    """ Nice print of json data, useful for debugging
    """
    try:
        print(data, indent=4, sort_keys=True)
    except TypeError:
        print(json.dumps(data, indent=4, sort_keys=True))

def get_data(url):
    """ Discodata query
    """
    response = requests.get(url)
    data = json.loads(response.text)

    return data['results']

def adapt_field(field):
    """ Convert sql field name to application field
    """
    if field in fields.keys():
        return fields[field]
    return field

def adapt_fields(data):
    """ Convert results list from sql to application format
    """
    res = []
    for item in data:
        adapted = {}
        for field in item.keys():
            adapted[adapt_field(field)] = item[field]
        res.append(adapted)
    return res

def import_from_discodata():
    """ Get data from discodata
    """
    vw_master = get_data(sql_views['vw_master'])
    master_data = adapt_fields(vw_master)

    # nice_print(master_data)
    # import pdb; pdb.set_trace()

    # for sql_view in sql_views.items():
    #     url = sql_view[1]
    #     response = len(get_data(url)['results'])
    #     print(response)

if __name__ == "__main__":
    import_from_discodata()
