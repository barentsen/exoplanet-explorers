"""Create a summary of the classifications by subject, i.e. produce
a new table with one row per planet candidate that summarizes the
number of times a user said 'yes'.
"""
import pandas as pd
import numpy as np
from astropy import units as u
from tqdm import tqdm

INPUT_FN = '../output/classifications-easy-format.csv'
OUTPUT_REAL_FN = '../output/summary-real-candidates.csv'
OUTPUT_SIM_FN = '../output/summary-simulations.csv'


if __name__ == '__main__':
    # Read the classification table
    classifications = pd.read_csv(INPUT_FN, dtype={'candidatename': str})

    # Produce a report card
    report = '#Users: {}\n'.format(classifications['user_name'].unique().size)
    report += '#Classifications: {}\n'.format(len(classifications))
    report += '#Subjects: {}\n'.format(classifications['subject_id'].unique().size)
    report += '#Classifications/subject (median): {}\n'.format(classifications.groupby('subject_id')['subject_id'].count().median())
    report += '#Candidates classified: {}\n'.format((~classifications.sim).sum())
    report += '#Simulations classified: {}\n'.format(classifications.sim.sum())
    print(report)
    reportcard = open('../output/reportcard.txt', 'w')
    reportcard.write(report)
    reportcard.close()

    # Produce a summary table containing one row per planet candidate
    rows = []
    for group in tqdm(classifications.groupby('subject_id'), desc='Writing summary table'):
        n_classifications = len(group[1])
        n_yes = (group[1]['response'] == 'Yes').sum()
        n_no = (group[1]['response'] == 'No').sum()
        assert(n_classifications == (n_yes + n_no))
        row = {'subject_id': group[0],
               'epic': group[1]['candidatename'].iloc[0].split('.')[0].strip(),
               'candidatename': group[1]['candidatename'].iloc[0],
               'sim': group[1]['sim'].iloc[0],
               'per': group[1]['per'].iloc[0],
               'n_classifications': n_classifications,
               'n_yes': n_yes,
               'n_no': n_no,
               'percent_yes': 100. * n_yes / n_classifications
               }
        rows.append(row)

    # Write the summaries to csv for real candidates and simulations separately
    col_order = ['subject_id', 'epic', 'candidatename', 'n_classifications', 'n_yes', 'n_no', 'percent_yes']
    summary = pd.DataFrame(rows)
    mask_sim = summary.sim
    summary_sim = summary[mask_sim]
    summary_real = summary[~mask_sim]
    summary_sim[col_order].to_csv(OUTPUT_SIM_FN, index=False)
    summary_real[col_order].to_csv(OUTPUT_REAL_FN, index=False)
