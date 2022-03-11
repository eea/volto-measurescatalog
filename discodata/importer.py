#!/usr/bin/env python3

import csv
import json
import os
from collections import defaultdict

import tqdm
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

OM = 'Origin of the measure'




import requests

def read_details_csv_files(location):
    data = defaultdict(list)

    fnames = [f for f in os.listdir(location)
              if f.endswith('csv') and f != 'master.csv']
    for name in fnames:
        with open(os.path.join(location, name)) as f:
            reader = iter(csv.reader(f))

            headers = None
            for line in reader:
                headers = line
                break

            index = headers.index('Origin of the measure')

            for line in reader:
                items = zip([h.strip() for h in headers], line)
                item = dict(items)
                item['_id'] = get_id(item)
                data[line[index]].append(item)
                fix_misspellings(item)

    res = {}
    for index, items in data.items():
        res[index] = dict(zip([item['_id'] for item in items], items))

    return res


def read_master_csv_files(location):
    data = []
    with open(os.path.join(location, 'master.csv')) as f:
        reader = iter(csv.reader(f))

        headers = None
        for line in reader:
            headers = line
            break

        for line in reader:
            items = zip([h.strip() for h in headers], line)
            item = dict(items)
            item['_id'] = get_id(item)
            data.append(item)
            fix_misspellings(item)

    return data


def fix_descriptor(rec):
    descriptors = [f'D{n}' for n in range(1, 12)]
    s = []
    for d in descriptors:
        if rec[d] == '1':
            s.append(d)
        del rec[d]
    rec['Descriptors'] = s


def fix_impacts(rec):
    s = []
    fields = [
        'IMPACTS Waste management', 'IMPACTS Air pollution',
        'IMPACTS Marine litter', 'IMPACTS NIS', 'IMPACTS Noise',
        'IMPACTS Pollution', 'IMPACTS Water pollution', 'IMPACTS Other'
    ]
    for f in fields:
        if f in rec:
            if rec[f] == '1':
                s.append(f.replace('IMPACTS ', ''))
            del rec[f]
    rec['Impacts'] = s


def fix_region(rec):
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
    s = []

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
    for f in fields:
        if f in rec:
            if rec[f] == '1':
                s.append(f)
            del rec[f]
    rec['Keywords'] = s


def get_id(rec):
    if rec.get('MeasureCode'):
        return rec['MeasureCode']
    if rec.get('CodeCatalogue'):
        return rec['CodeCatalogue']


def remap(k):
    if k == 'Feature Name':
        k = 'Feature name'

    return k


def fix_misspellings(rec):
    for k, v in rec.items():
        if v == 'Nos specified':
            rec[k] = 'Not specified'
        rec[k] = rec[k].strip()
        # if rec[k].endswith('\n'):


def make_mappings(data):
    blacklist = ['_id', "_index"]
    fields = set()
    for line in data:
        for k in line.keys():
            fields.add(k)

    mapping = {}
    for f in fields:
        if f not in blacklist:
            mapping[f] = {"type": "keyword",
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


# def fix_fieldnames(rec):
    # for k, v in rec.items():
    #     k = k.replace(' ', '_').replace('(', '').replace(')')


def main():
    host = 'localhost'
    # host = '10.50.4.114'
    # host = '10.50.4.82'
    index = 'wise_catalogue_measures'

    # with open('./analyzers.json') as f:
    #     analyzers = json.loads(f.read())

    conn = Elasticsearch([host])
    master_data = read_master_csv_files('./csv')

    data = read_details_csv_files('./csv')

    for (i, main) in enumerate(master_data):
        measure_name = main[OM]
        rec = data[measure_name][main['_id']]

        keys = main.keys()
        for k, v in rec.items():
            # uses the key from master record
            for mk in keys:
                if k.lower().strip() == mk.lower().strip():
                    k = mk
            k = remap(k)
            if k in main \
                    and main[k] \
                    and main[k].lower() != v.lower():
                print(
                    f"Data conflict at position: : {i} ({main['_id']})")
                print(f"Key: {k}. Conflicting sheet: {measure_name}.")
                print(f"Master value: <{main[k]}>. Sheet value: <{v}>")
                print("")
            else:
                main[k] = v

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

# NEW ------------------

def get_data(url):
    f = requests.get(url)
    data = json.loads(f.text)
    print(json.dumps(data, indent=4, sort_keys=True))

    return data

def import_from_discodata():
    # SQL Views
    # [vw_master_BD_2013_2018]
    # [vw_master_HD_Habitats_2013_2018_Filtered]
    # [vw_master_HD_Species_2013_2018_Filtered]
    # [vw_master_MSFD_Filtered]
    # [vw_master_MSPD]
    # [vw_master_Sectorial]
    # [vw_master_WFD_Filtered]
    # [vw_master]

    # OK Select * from [WISE_ShippingsPorts_Measures].[latest].vw_master_BD_2013_2018
    # ?? Select * from [WISE_ShippingsPorts_Measures].[latest].vw_master_HD_Habitats_2013_2018_Filtered
    # ?? Select * from [WISE_ShippingsPorts_Measures].[latest].vw_master_HD_Species_2013_2018_Filtered
    # OK Select * from [WISE_ShippingsPorts_Measures].[latest].vw_master_MSFD_Filtered
    # OK Select * from [WISE_ShippingsPorts_Measures].[latest].vw_master_MSPD
    # ?? Select * from [WISE_ShippingsPorts_Measures].[latest].vw_master_Sectorial
    # OK Select * from [WISE_ShippingsPorts_Measures].[latest].vw_master_WFD_Filtered
    # ?? Select * from [WISE_ShippingsPorts_Measures].[latest].vw_master

    sql_views = {
        'vw_master_BD_2013_2018': 'https://discodata.eea.europa.eu/sql?query=Select%20*%20from%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.vw_master_BD_2013_2018&p=1&nrOfHits=100&mail=null&schema=null',
        'vw_master_HD_Habitats_2013_2018_Filtered': 'https://discodata.eea.europa.eu/sql?query=Select%20*%20from%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.vw_master_HD_Habitats_2013_2018_Filtered%0A&p=1&nrOfHits=100&mail=null&schema=null',
        'vw_master_HD_Species_2013_2018_Filtered': 'https://discodata.eea.europa.eu/sql?query=Select%20*%20from%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.vw_master_HD_Species_2013_2018_Filtered%0A&p=1&nrOfHits=100&mail=null&schema=null',
        'vw_master_MSFD_Filtered': 'https://discodata.eea.europa.eu/sql?query=Select%20*%20from%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.vw_master_MSFD_Filtered%0A&p=1&nrOfHits=100&mail=null&schema=null',
        'vw_master_MSPD': 'https://discodata.eea.europa.eu/sql?query=Select%20*%20from%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.vw_master_MSPD%0A&p=1&nrOfHits=100&mail=null&schema=null',
        'vw_master_Sectorial': 'https://discodata.eea.europa.eu/sql?query=Select%20*%20from%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.vw_master_Sectorial%0A&p=1&nrOfHits=100&mail=null&schema=null',
        'vw_master_WFD_Filtered': 'https://discodata.eea.europa.eu/sql?query=Select%20*%20from%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.vw_master_WFD_Filtered%0A&p=1&nrOfHits=100&mail=null&schema=null',
        'vw_master': 'https://discodata.eea.europa.eu/sql?query=Select%20*%20from%20%5BWISE_ShippingsPorts_Measures%5D.%5Blatest%5D.vw_master%0A&p=1&nrOfHits=100&mail=null&schema=null',
    }

    host = 'localhost'
    # host = '10.50.4.114'
    # host = '10.50.4.82'
    index = 'wise_catalogue_measures'

    # with open('./analyzers.json') as f:
    #     analyzers = json.loads(f.read())

    conn = Elasticsearch([host])

    for sql_view in sql_views.keys():
        x = get_data(sql_views[sql_view])

    print("WIP DONE")

    """
        vw_master_BD_2013_2018
            catalogueCode
            sector
            useOrActivity
            measureName
            status
            measureOrigin
            measureNature
            waterBodyCategory
            spatialScope
            country
            measureImpactTo
            measureImpactToDetails
            D1
            D2
            D3
            D4
            D5
            D6
            D7
            D8
            D9
            D10
            D11
        vw_master_HD_Habitats_2013_2018_Filtered
            TODO
        vw_master_HD_Species_2013_2018_Filtered
            TODO
        vw_master_MSFD_Filtered
            catalogueCode
            sector
            useOrActivity
            measureName
            status
            measureOrigin
            measureNature
            waterBodyCategory
            spatialScope
            country
            measureImpactTo
            measureImpactToDetails
            D1
            D2
            D3
            D4
            D5
            D6
            D7
            D8
            D9
            D10
            D11
        vw_master_MSPD
            catalogueCode
            sector
            useOrActivity
            measureName
            status
            measureOrigin
            measureNature
            waterBodyCategory
            spatialScope
            country
            measureImpactTo
            measureImpactToDetails
            D1
            D2
            D3
            D4
            D5
            D6
            D7
            D8
            D9
            D10
            D11
        vw_master_Sectorial
            TODO
        vw_master_WFD_Filtered
            catalogueCode
            sector
            useOrActivity
            measureName
            status
            measureOrigin
            measureNature
            waterBodyCategory
            spatialScope
            country
            measureImpactTo
            measureImpactToDetails
            D1
            D2
            D3
            D4
            D5
            D6
            D7
            D8
            D9
            D10
            D11
        vw_master
            TODO
    """

if __name__ == "__main__":
    # main()
    import_from_discodata()

    """
    (Pdb) data.keys()
    dict_keys(['Sectorial', 'BD (Directive 79/409/EEC)', 'WFD (Directive 2000/60/EC)', 'MSPD (Directive 2008/56/EC)', 'HD (Directive 92/43/EEC)', 'MSFD (Directive 2008/56/EC)'])
    data
        ['Sectorial']
            ['SEC01']
                {
                    'MeasureCode': 'SEC01',
                    'Measure': 'Strengthening release standards and banning the most toxic substances',
                    'Sector': 'Shipping',
                    'Use or activity': 'not specified',
                    'Nature': 'legislation/regulation',
                    'IMPACTS Waste management': '0',
                    'IMPACTS Air pollution': '0',
                    'IMPACTS Marine litter': '0',
                    'IMPACTS NIS': '0',
                    'IMPACTS Noise': '0',
                    'IMPACTS Pollution': '1',
                    'IMPACTS Water pollution': '1',
                    'IMPACTS Other': '0',
                    'Measure impacts to':
                    'Not specified',
                    'Status': 'not specified',
                    'Spatial scale': 'Not specified',
                    'Spatial scope': 'Not specified',
                    'Water body': 'Not specified',
                    'Origin of the measure': 'Sectorial',
                    'Source(s)': 'SHEBA 2018, Policy Brief - Polic',
                    'D1': '0',
                    'D2': '0',
                    'D3': '0',
                    'D4': '0',
                    'D5': '0',
                    'D6': '0',
                    'D7': '0',
                    'D8': '1',
                    'D9': '1',
                    'D10': '0',
                    'D11': '0',
                    'TOTAL': '2',
                    '_id': 'SEC01'

                }
        ['BD (Directive 79/409/EEC)']
            ['BD1924']
                {
                    'MeasureCode': 'BD1924',
                    'Sector': 'Ports and traffic',
                    'Use or activity': 'not specified',
                    'Region': '',
                    'Country_code': 'ES',
                    'Country': 'Spain',
                    'Season': 'B',
                    'Measure Impacts to': 'Birds',
                    'Feature code': 'A850',
                    'Feature name': 'Calonectris diomedea s. str.',
                    'Sub-unit': 'sensu stricto [excluding borealis]',
                    'Water body': 'Not specified',
                    'Pressure code': 'E02',
                    'Pressure name': 'Shipping lanes and ferry lanes transport operations',
                    'Pressure type': 't',
                    'Pressure location': 'inOutEU',
                    'Ranking': 'M',
                    'Measure code': 'CE01',
                    'Measure name': 'Reduce impact of transport operation and infrastructure',
                    'Measure type recommended to address E02 and/or E03': '1',
                    'measure purpose': '',
                    'Measure location': '',
                    'Measure response': '',
                    'Measure status': 'ident',
                    'Origin of the measure': 'BD (Directive 79/409/EEC)',
                    'Nature of the measure': 'not specified',
                    'Spatial scope': 'not specified',
                    'Measure additional info': 'En este apartado sería necesario incluir las siguientes: CX02 y CS03',
                    'D1': '1',
                    'D2': '0',
                    'D3': '0',
                    'D4': '0',
                    'D5': '0',
                    'D6': '1',
                    'D7': '0',
                    'D8': '0',
                    'D9': '0',
                    'D10': '0',
                    'D11': '0',
                    'TOTAL_impacts': '0',
                    '_id': 'BD1924'
                }
    """
