import json
import os
import pandas
import sys

def clean_case_studies(file_location):
    diagnoses_columns = ['year_of_diagnosis', 'age_at_diagnosis', 'days_to_last_follow_up', 'tumor_grade', 'days_to_recurrence', 'prior_malignancy']
    demographic_columns = ['gender', 'race', 'vital_status', 'ethnicity', 'days_to_death', 'days_to_birth', 'year_of_birth', 'cause_of_death']
    base_columns = ['disease_type', 'primary_site']

    data = pandas.read_json(file_location)

    # We're primarily going to be interested in analysis based off of diagnoses and demographic info, drop missing rows
    trimmed = data.dropna(subset=['diagnoses', 'demographic', 'primary_site'])

    # Diagnoses gets injested as a Series of length 1, flatten it out so that we can easily process as object
    trimmed['diagnoses'] = trimmed['diagnoses'].apply(lambda x: x[0])

    # List comprehension over object keys is significantly faster than pandas' json_normalize utility
    trimmed[diagnoses_columns] = pandas.DataFrame([x for x in trimmed['diagnoses']])[diagnoses_columns]
    trimmed[demographic_columns] = pandas.DataFrame([x for x in trimmed['demographic']])[demographic_columns]

    # Trimmed has a llllot of noisy columns that we won't use, lets scrub out ids and other noise
    clean = trimmed[base_columns + demographic_columns + diagnoses_columns]

    current_path = os.path.dirname(__file__)
    clean.to_json(f'{current_path}/processed/case_studies_clean.json')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('Missing file location parameter')

    clean_case_studies(sys.argv[1])