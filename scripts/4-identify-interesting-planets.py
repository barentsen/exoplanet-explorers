"""Rough script to identify interesting planets given some criteria."""
import pandas as pd
import numpy as np

# List interesting subjects to be ignored (visually checked to be noise)
#BLACKLIST = [8496145, 8496408, 8502417, 8502526, 8502603, 8503527, 8503858,
#             8504735, 8504867, 8504889, 7616406]


if __name__ == '__main__':
    df = pd.read_csv('../output/summary-with-parameters.csv')

    # Strong candidates are defined as having high S/N and >3 'yes' votes
    mask_strong_candidates = (
                                (df.n_classifications > 4) &
                                (df.n_yes / df.n_classifications > 0.7) &
                                (df.fit_s2n > 1) &
                                (df.Rearth < 11.2)
                             )
    strong_candidates = df[mask_strong_candidates]
    strong_candidates.to_csv('../output/strong-planet-candidates.csv', index=False)
    print('Found {} strong candidates.'.format(mask_strong_candidates.sum()))

    # Interesting new planets are strong candidates in C10/C12
    # which may be rocky and in the HZ
    mask_interesting_new = (
                                mask_strong_candidates &
                                df.campaign.isin(['k2c10_stparas.txt', 'k2c12_stparas.txt']) &
                                (df.Rearth < 2)
                            )
    interesting_new = df[mask_interesting_new]
    interesting_new.to_csv('../output/interesting-new-planet-candidates.csv', index=False)
    print('Found {} interesting new candidates.'.format(mask_interesting_new.sum()))

    print(interesting_new)

"""
 &
                                (df.a > (0.7*np.sqrt(df.luminosity))) &
                                (df.a < (1.8*np.sqrt(df.luminosity)))
"""