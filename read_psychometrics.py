import pandas as pd
import numpy as np

pmetrics = pd.read_excel("./NKI-merged demographic and assessment data_5.28.19.xlsx", sheet_name='NeuropsychTesting')
conn_key = pd.read_csv("./connectivity/conn_key")
for idx, row in conn_key.iterrows():
    conn_key.loc[idx, 'ID'] = "A000" + str(conn_key.loc[idx, 'ID'])
scores = pd.read_csv("./out.tsv", sep="\t")
scores = pd.merge(scores, conn_key, how='right', on='ID')
"""
all = pd.DataFrame()
scores = pd.read_csv("./out.tsv", sep="\t")
#feats = pd.read_csv("Neuropsych_features.txt")
sht = pmetrics
#drop complete duplicates
sht = sht.drop_duplicates()
#adjust ID column name
sht = sht.rename(columns={'Unnamed: 0': 'ID'})
#adjust column names
temp = sht.columns
print(temp[1:])
for col in temp[1:]:
    print(sht[col][0])
    if pd.notna(sht[col][0]):
        sht = sht.rename(columns={col: sht[col][0]})
#select only rows for subjects that we have scores for
sht = pd.merge(scores['ID'], sht, how='left', on='ID')
#all = all.drop_duplicates(subset='ID') #when there's a duplicate ID, taking the first row with that ID
print(sht[feats.data])
#all[feat_cols].to_csv("full_subset.csv")
"""
#scores = pd.read_csv("./out.tsv", sep="\t")
pmetrics = pmetrics.rename(columns={'Unnamed: 0': 'ID'})
#print(pmetrics)
"""
temp = pmetrics.columns
print(temp[1:])
for col in temp[1:]:
    print(pmetrics[col][0])
    if pd.notna(pmetrics[col][0]):
        pmetrics = pmetrics.rename(columns={col: pmetrics[col][0]})
"""
#neurofeedbac = pmetrics['Sub Study Label']=='Neurofeedbac'
#print(pmetrics[neurofeedbac])
#eventsfeedbac = pd.merge(scores['ID'], pmetrics[neurofeedbac], how='left', on='ID')
#print(eventsfeedbac)

pmetrics = pd.merge(scores['ID'], pmetrics, how='left', on='ID')
print(pmetrics)
pmetrics = pmetrics.dropna(axis='columns')
#with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#    print(pmetrics)
print(pmetrics.columns)
pmetrics = pmetrics.select_dtypes(include=np.number)
#with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#    print(pmetrics)
#rel.to_csv("neuropsych_testing.csv", index=False)
#print(rel)