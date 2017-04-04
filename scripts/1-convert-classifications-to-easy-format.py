"""Convert the dump of K2 planet classifications obtained from
the Zooniverse's Exoplanet Explorers into a simplified csv table."""

import json
import pandas as pd
from tqdm import tqdm

INPUT_FN = '../data/classifications-v20170405.csv'  # Standard 'classification export' file
OUTPUT_FN = '../output/classifications-easy-format.csv'


if __name__ == '__main__':
    df = pd.read_csv(INPUT_FN)

    # Run over each classification and extract the most useful fields
    rows = []
    for classification in tqdm(df.iterrows()):
        response = json.loads(classification[1]['annotations'])[0]['value']
        if response not in ['Yes', 'No']:
            continue  # Ignore early versions of the workflow

        subject_id = classification[1]['subject_ids']
        subject_data = json.loads(classification[1]['subject_data'])[str(subject_id)]

        row = {
                'classification_id': classification[1]['classification_id'],
                'subject_id': subject_id,
                'candidatename': subject_data['cand'],
                'response': response,
                'sim': subject_data['#sim'],
                'per': subject_data['per'],
                'user_name': classification[1]['user_name']
               }
        rows.append(row)

    # Create a new dataframe from the useful fields and export to csv
    df = pd.DataFrame(rows)
    col_order = ['classification_id', 'subject_id', 'candidatename', 'response',
                 'sim', 'per', 'user_name']
    df[col_order].to_csv(OUTPUT_FN, index=False)
