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

sql_further_information_views = {
    'BD_2013_2018': 'BD (Directive 79/409/EEC)',
    'HD_Habitats_2013_2018_Filtered': 'HD (Directive 92/43/EEC)', # ??
    'HD_Species_2013_2018_Filtered': 'HD (Directive 92/43/EEC)',  # ??
    'MSFD_Filtered': 'MSFD (Directive 2008/56/EC)',
    'MSPD': 'MSPD (Directive 2008/56/EC)',
    'Sectorial': 'Sectorial',
    'WFD_Filtered': 'WFD (Directive 2000/60/EC)',
}

sql_views_more = {
    'BD_2013_2018': {
        'url': 'https://discodata.eea.europa.eu/sql?query=SELECT%20*%20FROM%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.%5BBD_2013_2018%5D&p=1&nrOfHits=1000000&mail=null&schema=null',
        'fields': [
            'catalogueCode',
            'sectorId',
            'useOrActivityId',
            'countryCode',
            'waterBodyCategoryId',
            'measureStatusId',
            'measureOriginId',
            'measureNatureId',
            'spatialScopeId',
            'measureImpactToId',
            'measureImpactToDetails',
            'measureName',
            'pressureCode',
            'pressureName',
            'pressureType',
            'ranking',
            'measureCode',
            'recommendedMeasureTypeE02AndOrE03',
            'measurePurpose',
            'measureLocation',
            'measureResponse',
            'measureAdditionalInfo',
            'season',
            'featureCode',
            'subUnit',
        ]
    },
    'HD_Habitats_2013_2018_Filtered': {
        'url': 'https://discodata.eea.europa.eu/sql?query=SELECT%20*%20FROM%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.%5BHD_Habitats_2013_2018_Filtered%5D&p=1&nrOfHits=1000000&mail=null&schema=null',
        'fields': [
            'catalogueCode',
            'sectorId',
            'useOrActivityId',
            'countryCode',
            'waterBodyCategoryId',
            'measureName',
            'measureStatusId',
            'measureOriginId',
            'measureNatureId',
            'spatialScopeId',
            'measureImpactToId',
            'measureImpactToDetails',
        ]
    },
    'HD_Species_2013_2018_Filtered': {
        'url': 'https://discodata.eea.europa.eu/sql?query=SELECT%20*%20FROM%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.%5BHD_Species_2013_2018_Filtered%5D&p=1&nrOfHits=1000000&mail=null&schema=null',
        'fields': [
            'catalogueCode',
            'countryCode',
            'measureImpactToDetails',
            'measureImpactToId',
            'measureNatureId',
            'measureOriginId',
            'measureStatusId',
            'sectorId',
            'spatialScopeId',
            'useOrActivityId',
            'waterBodyCategoryId',
            'measureName',
            'featureCode',
            'pressureCode',
            'pressureName',
            'pressureType',
            'ranking',
            'measureCode',
            'recommendedMeasureTypeE02AndOrE03',
            'measurePurpose',
            'measureLocation',
            'measureResponse',
            'measureAdditionalInfo',
        ]
    },
    'MSFD_Filtered': {
        'url': 'https://discodata.eea.europa.eu/sql?query=SELECT%20*%20FROM%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.%5BMSFD_Filtered%5D&p=1&nrOfHits=1000000&mail=null&schema=null',
        'fields': [
            'catalogueCode',
            'countryCode',
            'measureName',
            'useOrActivityId',
            'measureImpactToId',
            'waterBodyCategoryId',
            'spatialScopeId',
            'measureOriginId',
            'measureNatureId',
            'sectorId',
            'measureStatusId',
            'measureImpactToDetails',
            'measureNumber',
            'existingPoliciesLink',
            'ktmLinkTo',
            'relevantTargets',
            'descriptorsItLinksTo',
            'relevantFeaturesFromAnnexIII',
            'otherSpatialScope',
        ],
    },
    'MSPD': {
        'url': 'https://discodata.eea.europa.eu/sql?query=SELECT%20*%20FROM%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.%5BMSPD%5D&p=1&nrOfHits=1000000&mail=null&schema=null',
        'fields': [
            'catalogueCode',
            'countryCode',
            'waterBodyCategoryId',
            'measureStatusId',
            'measureOriginId',
            'measureNatureId',
            'spatialScopeId',
            'measureImpactToId',
            'sectorId',
            'useOrActivityId',
            'measureImpactToDetails',
            'measureName',
            'implementationStatus',
            'shippingTackled',
            'trafficSeparationScheme',
            'priority',
            'approachingAreas',
            'precautionaryAreas',
            'areasToBeAvoided',
            'futureScenarios',
            'source',
            'keywords',
            'authority',
            'generalView',
            'ports',
            'futureExpectations',
            'safetyManner',
            'objective',
            'categories',
        ]
    },
    'Sectorial': {
        'url': 'https://discodata.eea.europa.eu/sql?query=SELECT%20*%20FROM%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.%5BSectorial%5D&p=1&nrOfHits=1000000&mail=null&schema=null',
        'fields': [
            'catalogueCode',
            'countryCode',
            'measureImpactToDetails',
            'measureImpactToId',
            'measureNatureId',
            'measureOriginId',
            'measureStatusId',
            'sectorId',
            'spatialScopeId',
            'useOrActivityId',
            'waterBodyCategoryId',
            'measureName',
            'source',
        ]
    },
    'WFD_Filtered': {
        'url': 'https://discodata.eea.europa.eu/sql?query=SELECT%20*%20FROM%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.%5BWFD_Filtered%5D&p=1&nrOfHits=1000000&mail=null&schema=null',
        'fields': [
            'catalogueCode',
            'sectorId',
            'useOrActivityId',
            'physicalModificationNature',
            'hydromorphologyEffect',
            'ecologicalImpact',
            'measureMitigationGEP',
            'countryCode',
            'waterBodyCategoryId',
            'measureStatusId',
            'measureOriginId',
            'measureNatureId',
            'spatialScopeId',
            'measureImpactToId',
            'measureImpactToDetails',
        ]
    }
}

spatial_scopes_view = "https://discodata.eea.europa.eu/sql?query=SELECT%20TOP%20100%20*%20FROM%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.%5BSpatial_scopes%5D&p=1&nrOfHits=100&mail=null&schema=null"

app_fields = {
    'D1': 'D1',
    'D10': 'D10',
    'D11': 'D11',
    'D2': 'D2',
    'D3': 'D3',
    'D4': 'D4',
    'D5': 'D5',
    'D6': 'D6',
    'D7': 'D7',
    'D8': 'D8',
    'D9': 'D9',
    'catalogueCode': 'CodeCatalogue',
    'country': 'Country',
    'measureImpactTo': 'Measure Impacts to',
    'measureImpactToDetails': 'Measure Impacts to (further details)',
    'measureName': 'Measure name',
    'measureNature': 'Nature of the measure',
    'measureOrigin': 'Origin of the measure',
    'sector': 'Sector',
    'spatialScope': 'Spatial scope',
    'status': 'Status',
    'useOrActivity': 'Use or activity',
    'waterBodyCategory': 'Water body category',

    # Further information
    'approachingAreas': 'Approaching Areas',
    'areasToBeAvoided': 'Areas to be avoided',
    'authority': 'Authority',
    'categories': 'Categories',
    'countryCode': '',
    'descriptorsItLinksTo': '',
    'ecologicalImpact': 'Ecological impacts',
    'existingPoliciesLink': 'Link to existing policies',
    'featureCode': '',
    'futureExpectations': 'Future Expectations',
    'futureScenarios': 'Future Scenarios',
    'generalView': 'General View',
    'hydromorphologyEffect': 'Effect on hydromorphology',
    'implementationStatus': 'MSPD implementation status',
    'keywords': 'Keywords',
    'ktmLinkTo': 'KTMs it links to',
    'measureAdditionalInfo': 'Measure additional info',
    'measureCode': '',
    'measureImpactToId': '',
    'measureLocation': 'Measure location',
    'measureMitigationGEP': '',
    'measureNatureId': '',
    'measureNumber': '',
    'measureOriginId': '',
    'measurePurpose': 'Measure purpose',
    'measureResponse': 'Measure response',
    'measureStatusId': '',
    'objective': 'Objective',
    'otherSpatialScope': 'MSFD Spatial scope',
    'physicalModificationNature': 'Nature of physical modification',
    'ports': 'Ports',
    'precautionaryAreas': 'Precautionary areas',
    'pressureCode': '',
    'pressureName': 'Pressure name',
    'pressureType': 'Pressure type',  # 'Type of pressure',
    'priority': 'Priority Areas',
    'ranking': 'Ranking',
    'recommendedMeasureTypeE02AndOrE03':
        'Measure type recommended to address E02 and/or E03',
    'relevantFeaturesFromAnnexIII': 'Relevant features from MSFD Annex III',
    'relevantTargets': 'Relevant targets',
    'safetyManner': 'Safety manner',
    'season': 'Season',
    'sectorId': '',
    'shippingTackled': 'Shipping Tackled',
    'source': 'Source',
    'spatialScopeId': 'Spatial scale',
    'subUnit': '',
    'trafficSeparationScheme': 'Traffic separation scheme',
    'useOrActivityId': '',
    'waterBodyCategoryId': '',
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
            mapping[field] = {
                "type": "keyword",
                "copy_to": ['all_fields_for_freetext', 'autocomplete', 'did_you_mean'],
            }

    mapping["autocomplete"] = {
        "analyzer": "autocomplete",
        "copy_to": ["all_fields_for_freetext"],
        "fielddata": True,
        "type": "text"
    }

    mapping["did_you_mean"] = {
        "analyzer": "didYouMean",
        "copy_to": ["all_fields_for_freetext"],
        "fielddata": True,
        "type": "text"
    }

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

def fix_spatial_scope(rec, spatial_scopes):
    """ Fix spatial scale
    """
    new = [x['name'] for x in spatial_scopes if x['Id'] == rec.get("Spatial scale")]
    if new is not None:
        rec["Spatial scale"] = new

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
        adapted_field = app_fields[field]
        if adapted_field != '':
            return adapted_field
    return field

def adapt_value(value):
    """ Convert sql field name to application field
    """
    if isinstance(value, int):
        return str(value)
    if value == "null":
        value = ""
    if value is None:
        value = ""
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

def get_further_information_data():
    """ Get data to be listed in Further information fields
    """
    res = {}
    for view, app_view in sql_further_information_views.items():
        if app_view not in res:
            res[app_view] = {}
        data = adapt_fields_and_values(get_data(sql_views_more[view]['url']))
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
    further_information_data = get_further_information_data()
    spatial_scopes = adapt_fields_and_values(get_data(spatial_scopes_view))

    for (i, main) in enumerate(master_data):
        measure_name = main[OM]
        rec = data[measure_name][main['_id']]
        rec_further = further_information_data[measure_name][main['_id']]

        for field in rec_further.keys() - rec.keys():
            if field != '':
                rec[field] = rec_further[field]

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
        fix_region(main)
        fix_spatial_scope(main, spatial_scopes)
        # fix_fieldnames(main)

        _id = get_id(main)
        main['_id'] = _id
        main['_index'] = index

    ids = set([rec['_id'] for rec in master_data])
    print(f"Unique records: {len(ids)}")

    resp = conn.indices.create(
        index,
        body={
            "settings": {
                "max_shingle_diff": "12",
                "analysis": {
                    "analyzer": {
                        "autocomplete": {
                            "char_filter": [
                                "html_strip"
                            ],
                            "filter": [
                                "lowercase",
                                "stop",
                                "autocompleteFilter",
                                "trim"
                            ],
                            "tokenizer": "standard",
                            "type": "custom"
                        },
                        "comma": {
                            "lowercase": "false",
                            "pattern": ", ",
                            "type": "pattern"
                        },
                        "date2year": {
                            "pattern": "[-](.*)",
                            "type": "pattern"
                        },
                        "default": {
                            "filter": [
                                "lowercase",
                                "stop",
                                "asciifolding",
                                "english_stemmer"
                            ],
                            "tokenizer": "standard",
                            "type": "custom"
                        },
                        "didYouMean": {
                            "char_filter": [
                                "html_strip"
                            ],
                            "filter": [
                                "lowercase"
                            ],
                            "tokenizer": "standard",
                            "type": "custom"
                        },
                        "english_stop_analyzer": {
                            "filter": [
                                "english_stop"
                            ],
                            "tokenizer": "lowercase"
                        },
                        "freetext": {
                            "char_filter": [
                                "html_strip"
                            ],
                            "filter": [
                                "lowercase",
                                "english_stop"
                            ],
                            "tokenizer": "standard",
                            "type": "custom"
                        },
                        "highlight": {
                            "filter": [
                                "lowercase",
                                "asciifolding"
                            ],
                            "tokenizer": "standard",
                            "type": "custom"
                        },
                        "none": {
                            "filter": [
                                "lowercase"
                            ],
                            "type": "keyword"
                        },
                        "semicolon": {
                            "lowercase": "false",
                            "pattern": "; ",
                            "type": "pattern"
                        }
                    },
                    "char_filter": {
                        "url_filter": {
                            "mappings": [
                                "/ =>  ",
                                ". =>  "
                            ],
                            "type": "mapping"
                        }
                    },
                    "filter": {
                        "autocompleteFilter": {
                            "filler_token": "",
                            "max_shingle_size": "12",
                            "min_shingle_size": "2",
                            "type": "shingle"
                        },
                        "english_stemmer": {
                            "language": "english",
                            "type": "stemmer"
                        },
                        "english_stop": {
                            "stopwords": [
                                "a",
                                "an",
                                "and",
                                "are",
                                "as",
                                "at",
                                "be",
                                "but",
                                "by",
                                "for",
                                "if",
                                "in",
                                "into",
                                "is",
                                "it",
                                "no",
                                "not",
                                "of",
                                "on",
                                "or",
                                "such",
                                "that",
                                "the",
                                "their",
                                "then",
                                "there",
                                "these",
                                "they",
                                "this",
                                "to",
                                "was",
                                "will",
                                "what",
                                "when",
                                "where",
                                "which",
                                "who",
                                "how",
                                "why",
                                "does"
                            ],
                            "type": "stop"
                        }
                    },
                },
            },
            "mappings": {
                "properties": make_mappings(master_data)
            },

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
