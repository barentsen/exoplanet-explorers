"""Rough script to identify interesting planets given some criteria."""
import pandas as pd

# List interesting subjects to be ignored (visually checked to be noise)
BLACKLIST = [8496145, 8496408, 8502417, 8502526, 8502603, 8503527, 8503858,
             8504735, 8504867, 8504889, 7616406]


if __name__ == '__main__':
    df = pd.read_csv('../output/summary-with-parameters.csv')
    mask = ((df.n_classifications > 1)
            & (df.n_yes > 1)
            & (df.campaign == 'k2c10_stparas.txt')
            & (df.fit_s2n > 10)
            & (df.Rearth < 2)
            & (df.in_hz)
            & (~df.subject_id.isin(BLACKLIST))
           )
    print('Found {} candidates.'.format(mask.sum()))
    print(df[mask])
