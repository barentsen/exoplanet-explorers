import pandas as pd
import matplotlib.pyplot as pl

df = pd.read_csv('../output/strong-planet-candidates.csv')

pl.figure()
counts, edges, patches = pl.hist(df.Rearth, bins=[0.7, 1.4, 2.8, 5.7, 11.2])
pl.show()
pl.close()

print(counts)