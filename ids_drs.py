import pandas as pd
import numpy as np

df = pd.read_csv('sorted_doctors.csv')
df.drop('Unnamed: 0', axis=1, inplace=True)

names = pd.unique(df['NAME'].ravel())
names = pd.Series(np.arange(len(names)), names)

ranked = ( df['NAME'].rank(axis=0, method="dense").reshape(df.shape[0]).astype(int)-1 )
df.insert(0, 'DOC_ID', value=ranked)

df.to_csv('doc_sample.csv', index=False)

