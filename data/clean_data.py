import json
import os
import pandas
import sys

major_sites = {
    'adrenal_gland': 'Adrenal gland',
    'bile_duct': 'Bile duct',
    'bladder': 'Bladder',
    'blood': 'Blood',
    'bone': 'Bone',
    'bone_marrow': 'Bone Marrow',
    'brain': 'Brain',
    'breast': 'Breast',
    'cervix': 'Cervix',
    'colorectoral': 'Colorectoral',
    'esophagus': 'Esophagus',
    'eye': 'Eye',
    'head_and_neck': 'Head and neck',
    'kidney': 'Kidney',
    'liver': 'Liver',
    'lung': 'Lung',
    'lymph_nodes': 'Lymph nodes',
    'nervous_system': 'Nervous system',
    'ovary': 'Ovary',
    'pancreas': 'Pancreas',
    'pleura': 'Pleura',
    'prostate': 'Prostate',
    'skin': 'Skin',
    'soft_tissue': 'Soft tissue',
    'stomach': 'Stomach',
    'testis': 'Testis',
    'thymus': 'Thymus',
    'thyroid': 'Thyroid',
    'uterus': 'Uterus',
    'other': 'Other'
}

sites_dict = {
    'Bronchus and lung': major_sites['lung'],
    'Hematopoietic and reticuloendothelial systems': major_sites['other'], # maybe bone marrow? partially lymph related
    'Colon': major_sites['colorectoral'],
    'Spinal cord, cranial nerves, and other parts of central nervous system': major_sites['nervous_system'],
    'Unknown': major_sites['other'],
    'Prostate gland': major_sites['prostate'],
    'Uterus, NOS': major_sites['uterus'],
    'Liver and intrahepatic bile ducts': major_sites['liver'],
    'Connective, subcutaneous and other soft tissues': major_sites['soft_tissue'],
    'Thyroid gland': major_sites['thyroid'],
    'Rectum': major_sites['colorectoral'],
    'Other and ill-defined sites': major_sites['other'],
    'Corpus uteri': major_sites['uterus'],
    'Other and ill-defined digestive organs': major_sites['other'],
    'Heart, mediastinum, and pleura': major_sites['other'],
    'Cervix uteri': major_sites['cervix'],
    'Other and unspecified major salivary glands': major_sites['other'],
    'Lymph Nodes': major_sites['lymph_nodes'],
    'Bones, joints and articular cartilage of other and unspecified sites': major_sites['bone'],
    'Retroperitoneum and peritoneum': major_sites['other'], # abdominal
    'Other and ill-defined sites in lip, oral cavity and pharynx': major_sites['head_and_neck'],
    'Peripheral nerves and autonomic nervous system': major_sites['nervous_system'],
    'Bones, joints and articular cartilage of limbs': major_sites['bone'],
    'Small intestine': major_sites['other'],
    'Gallbladder': major_sites['other'],
    'Meninges': major_sites['other'],
    'Not Reported': major_sites['other'],
    'Anus and anal canal': major_sites['other'],
    'Eye and adnexa': major_sites['eye'],
    'Other and unspecified parts of biliary tract': major_sites['other'], # liver? bile duct?
    'Other and unspecified urinary organs': major_sites['other'],
    'Oropharynx': major_sites['head_and_neck'],
    'Other endocrine glands and related structures': major_sites['other'],
    'Larynx': major_sites['head_and_neck'],
    'Other and unspecified female genital organs': major_sites['other'],
    'Other and unspecified parts of tongue': major_sites['head_and_neck'],
    'Nasopharynx': major_sites['head_and_neck'],
    'Rectosigmoid junction': major_sites['colorectoral'],
    'Vagina': major_sites['other'],
    'Floor of mouth': major_sites['head_and_neck'],
    'Tonsil': major_sites['head_and_neck'],
    'Other and unspecified parts of mouth': major_sites['head_and_neck'],
    'Nasal cavity and middle ear': major_sites['head_and_neck'],
    'Penis': major_sites['other'],
    'Hypopharynx': major_sites['head_and_neck'],
    'Base of tongue': major_sites['head_and_neck'],
    'Ureter': major_sites['other'],
    'Gum': major_sites['head_and_neck'],
    'Vulva': major_sites['other'],
    'Lip': major_sites['other'],
    'Trachea': major_sites['other'],
    'Palate': major_sites['other'],
    'Other and unspecified male genital organs': major_sites['other'],
    'Renal pelvis': major_sites['kidney']
}

def convert_to_major_site(value):
    if value in sites_dict:
        return sites_dict[value]
    else:
        return value

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

    # There's a lot of different values for cancer types, let's limit to the major sites called out on GDC for now
    trimmed['major_site'] = trimmed['primary_site'].apply(convert_to_major_site)

    # Trimmed has a llllot of noisy columns that we won't use, lets scrub out ids and other noise
    clean = trimmed[base_columns + demographic_columns + diagnoses_columns + ['major_site']]

    current_path = os.path.dirname(__file__)
    clean.to_json(f'{current_path}/processed/case_studies_clean.json')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('Missing file location parameter')

    clean_case_studies(sys.argv[1])