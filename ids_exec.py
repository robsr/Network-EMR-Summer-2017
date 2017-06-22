import pandas as pd
import numpy as np

df = pd.read_csv('executives_data.csv')
print(df.columns)

names = pd.unique(df['EXECUTIVE NAME'].ravel())
names = pd.Series(np.arange(len(names)), names)

ranked = ( df['EXECUTIVE NAME'].rank(axis=0, method="dense").reshape(df.shape[0]).astype(int)-1 )
df.insert(0, 'EXEC_ID', value=ranked)
df = df.sort_values('EXECUTIVE NAME')
df.to_csv('exec_dataset.csv', index=False)


