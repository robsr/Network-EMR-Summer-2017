import pandas as pd

df = pd.read_csv('./Data(net)/doc_sample.csv')
df.drop('Unnamed: 0', axis=1, inplace=True)


for drname in df['NAME']:
    count=0
    for name in df['NAME']:
        if name == drname:
            count+=1
    if count == 7:
        print(drname)

# print(df.columns)
# print(df.head())

