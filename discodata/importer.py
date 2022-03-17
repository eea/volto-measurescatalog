""" Import data from Discodata
    https://discodata.eea.europa.eu/
    WISE_ShippingsPorts_Measures - latest
"""
#!/usr/bin/env python3

import json
import requests

import tqdm
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

OM = 'Origin of the measure'

sql_views = {
    # default nrOfHits is set to 100 when copy-pasting from discodata.eea.europa.eu
    # manually set to 1000000, larger enough for 4618 (or 4641) items in master_data
    'vw_master_BD_2013_2018':
        'https://discodata.eea.europa.eu/sql?query=' \
        'Select%20*%20from%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.' \
        'vw_master_BD_2013_2018&p=1&nrOfHits=1000000&mail=null&schema=null',
    'vw_master_HD_Habitats_2013_2018_Filtered':
        'https://discodata.eea.europa.eu/sql?query=' \
        'Select%20*%20from%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.' \
        'vw_master_HD_Habitats_2013_2018_Filtered%0A&p=1&nrOfHits=1000000&mail=null' \
        '&schema=null',
    'vw_master_HD_Species_2013_2018_Filtered':
        'https://discodata.eea.europa.eu/sql?query=' \
        'Select%20*%20from%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.' \
        'vw_master_HD_Species_2013_2018_Filtered%0A&p=1&nrOfHits=1000000&mail=null&' \
        'schema=null',
    'vw_master_MSFD_Filtered':
        'https://discodata.eea.europa.eu/sql?query=' \
        'Select%20*%20from%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.'\
        'vw_master_MSFD_Filtered%0A&p=1&nrOfHits=1000000&mail=null&schema=null',
    'vw_master_MSPD':
        'https://discodata.eea.europa.eu/sql?query=' \
        'Select%20*%20from%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.' \
        'vw_master_MSPD%0A&p=1&nrOfHits=1000000&mail=null&schema=null',
    'vw_master_Sectorial':
        'https://discodata.eea.europa.eu/sql?query=' \
        'Select%20*%20from%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.' \
        'vw_master_Sectorial%0A&p=1&nrOfHits=1000000&mail=null&schema=null',
    'vw_master_WFD_Filtered':
        'https://discodata.eea.europa.eu/sql?query=' \
        'Select%20*%20from%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.' \
        'vw_master_WFD_Filtered%0A&p=1&nrOfHits=1000000&mail=null&schema=null',
    'vw_master':
        'https://discodata.eea.europa.eu/sql?query=' \
        'Select%20*%20from%20%5BWISE_ShippingsPorts_Measures%5D.' \
        '%5Blatest%5D.vw_master%0A&p=1&nrOfHits=1000000&mail=null&schema=null',
}

sql_details_views = {
    'vw_master_BD_2013_2018': 'BD (Directive 79/409/EEC)',
    'vw_master_HD_Habitats_2013_2018_Filtered': 'HD (Directive 92/43/EEC)', # ??
    'vw_master_HD_Species_2013_2018_Filtered': 'HD (Directive 92/43/EEC)',  # ??
    'vw_master_MSFD_Filtered': 'MSFD (Directive 2008/56/EC)',
    'vw_master_MSPD': 'MSPD (Directive 2008/56/EC)',
    'vw_master_Sectorial': 'Sectorial',
    'vw_master_WFD_Filtered': 'WFD (Directive 2000/60/EC)',
}

app_fields = {
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
}

def make_mappings(data):
    """ Mappings
    """
    blacklist = ['_id', "_index"]
    fields = set()
    for line in data:
        for k in line.keys():
            fields.add(k)

    mapping = {}
    for field in fields:
        if field not in blacklist:
            mapping[field] = {"type": "keyword",
                          "copy_to": ['all_fields_for_freetext']}

    mapping['all_fields_for_freetext'] = {
        "type": "text", "analyzer": "standard"      # analyzer:freetext
    }
    return mapping

    # {
    # "Sector": {"type": "keyword"},
    # "did_you_mean": {"type": "text", "analyzer": "didYouMean"},
    # "autocomplete": {"type": "text", "analyzer": "autocomplete"},
    # "CodeCatalogue": {"type": "text", "analyzer": "none"},
    # "Use_or_activity": {"type": "text", "analyzer": "none",
    # "fielddata": True},
    # }

def fix_descriptor(rec):
    """ Fix Descriptors fiel
    """
    descriptors = [f'D{n}' for n in range(1, 12)]
    value = []
    for descriptor in descriptors:
        if rec[descriptor] == '1':
            value.append(descriptor)
        del rec[descriptor]
    rec['Descriptors'] = value


def fix_impacts(rec):
    """ Fix Impacts field
    """
    value = []
    fields = [
        'IMPACTS Waste management', 'IMPACTS Air pollution',
        'IMPACTS Marine litter', 'IMPACTS NIS', 'IMPACTS Noise',
        'IMPACTS Pollution', 'IMPACTS Water pollution', 'IMPACTS Other'
    ]
    for field in fields:
        if field in rec:
            if rec[field] == '1':
                value.append(field.replace('IMPACTS ', ''))
            del rec[field]
    rec['Impacts'] = value


def fix_region(rec):
    """ Fix Region field
    """
    regions = {
        "MATL": "Marine Atlantic Region",
        "MBAL": "Marine Baltic Region",
        "MBLS": "Marine Region Black Sea",
        "MMAC": "Marine Macaronesian Region",
        "MMED": "Marine Mediterranean Region	"
    }
    if 'Region' in rec and rec['Region']:
        rec['Region'] = regions[rec['Region']]


def fix_keywords(rec):
    """ Fix Keywords field
    """
    value = []

    if 'Keywords' in rec:
        rec['Keywords'] = list(
            filter(None, [k.strip() for k in rec['Keywords'].split(',')]))
        return

    fields = [
        'accident management', 'administrative', 'air pollution',
        'anchoring/mooring', 'awareness raising', 'ballast waters',
        'construction', 'dredging', 'EU policies', 'hull fouling',
        'international agreements', 'legislation/regulation', 'maintenence',
        'marine litter', 'navigation', 'NIS', 'noise', 'pollution',
        'regional sea convention', 'PSSA/ZMES', 'technical measures',
        'waste management', 'water pollution'
    ]
    for field in fields:
        if field in rec:
            if rec[field] == '1':
                value.append(field)
            del rec[field]
    rec['Keywords'] = value

def remap(k):
    """ Remap
    """
    if k == 'Feature Name':
        k = 'Feature name'

    return k

def get_id(rec):
    """ Return ID for given record item
    """
    possible_fields = [
        'MeasureCode', 'CodeCatalogue', 'catalogueCode'
    ]

    for field in possible_fields:
        if rec.get(field):
            return rec[field]

    return None

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
    if field in app_fields:
        return app_fields[field]
    return field

def adapt_value(value):
    """ Convert sql field name to application field
    """
    if isinstance(value, int):
        return str(value)
    return value

def adapt_fields_and_values(data):
    """ Convert results list from sql to application format
    """
    res = []
    for item in data:
        adapted = {}
        for field in item:
            adapted[adapt_field(field)] = adapt_value(item[field])
        adapted['_id'] = get_id(item)
        res.append(adapted)
    return res

def get_details_data():
    """ Get data from sql_views other than master
    """
    res = {}
    for view, app_view in sql_details_views.items():
        if app_view not in res:
            res[app_view] = {}
        data = adapt_fields_and_values(get_data(sql_views[view]))
        for item in data:
            res[app_view][item['_id']] = item
    return res

def import_from_discodata():
    """ Get data from discodata
    """
    host = 'localhost'
    # host = '10.50.4.114'
    # host = '10.50.4.82'
    index = 'wise_catalogue_measures'

    # with open('./analyzers.json') as f:
    #     analyzers = json.loads(f.read())

    conn = Elasticsearch([host])

    vw_master = get_data(sql_views['vw_master'])
    master_data = adapt_fields_and_values(vw_master)

    data = get_details_data()

    for (i, main) in enumerate(master_data):
        measure_name = main[OM]
        rec = data[measure_name][main['_id']]

        keys = main.keys()
        for key, value in rec.items():
            # uses the key from master record
            for mkey in keys:
                if key.lower().strip() == mkey.lower().strip():
                    key = mkey
            key = remap(key)
            if key in main \
                    and main[key] \
                    and main[key].lower() != value.lower():
                print(
                    f"Data conflict at position: : {i} ({main['_id']})")
                print(f"Key: {key}. Conflicting sheet: {measure_name}.")
                print(f"Master value: <{main[key]}>. Sheet value: <{value}>")
                print("")
            else:
                main[key] = value

        fix_descriptor(main)
        fix_impacts(main)
        fix_keywords(main)
        fix_region(main)
        # fix_fieldnames(main)

        _id = get_id(main)
        main['_id'] = _id
        main['_index'] = index

    ids = set([rec['_id'] for rec in master_data])
    print(f"Unique records: {len(ids)}")

    resp = conn.indices.create(
        index,
        body={
            "mappings": {
                "properties": make_mappings(master_data)
            }

        })
    assert resp.get('acknowledged') is True

    body = []
    for doc in master_data:
        body.append(json.dumps({"create": doc}))

    print(f"Indexing {len(master_data)} documents")
    num_docs = len(master_data)
    progress = tqdm.tqdm(unit="docs", total=num_docs)

    successes = 0

    for ok, action in streaming_bulk(
        client=conn, index=index, actions=iter(master_data),
    ):
        progress.update(1)
        successes += ok

    print("Indexed %d/%d documents" % (successes, num_docs))

if __name__ == "__main__":
    import_from_discodata()