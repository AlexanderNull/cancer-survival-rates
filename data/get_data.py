import requests
import json
import os
import sys
from pathlib import Path

SAVE_PATH = f"{os.path.dirname(__file__)}/raw"
SAVE_FILENAME = 'case_studies.json'
SAVE_FILE_LOCATION = f'{SAVE_PATH}/{SAVE_FILENAME}'

def get_data():
    sort = 'case_id'
    expand_fields = 'demographic,diagnoses,diagnoses.treatments,exposures,family_histories,follow_ups,follow_ups.molecular_tests'
    page_size = 1000
    page_start = 0

    results = []
    retry = 0

    print('Retrieving case studies from gdc.cancer.gov')

    while True:
        response = requests.get(f'https://api.gdc.cancer.gov/cases?sort={sort}&expand={expand_fields}&size={page_size}&from={page_start}')
        if response.status_code == 200:
            retry = 0
            data = response.json()

            hits = data['data']['hits']
            results += hits

            pagination = data['data']['pagination']
            if pagination['page'] >= pagination['pages']:
                print(f'Reached the end at page {pagination["page"]}')
                #reached the last page, got all data
                break

            page_start += page_size

        elif retry < 3:
            retry += 1
        else:
            # Couldn't proceed even with retrying api calls
            break

    print(f'Retrieved a total of {len(results)} results')
    return results

def save_data(results):
    with open(SAVE_FILE_LOCATION, 'w') as results_file:
        json.dump(results, results_file)

def gather_data(overwrite = False):
    if overwrite or not os.path.exists(SAVE_FILE_LOCATION):
        save_data(get_data())


if __name__ == '__main__':
    overwrite = None if len(sys.argv) == 1 else sys.argv[1]
    gather_data(overwrite)
