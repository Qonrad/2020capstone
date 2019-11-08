import pandas as pd
import numpy as np

#read my scores
scores = pd.read_csv("./out.tsv", sep="\t")
conn_key = pd.read_csv("./connectivity/conn_key")
for idx, row in conn_key.iterrows():
    conn_key.loc[idx, 'ID'] = "A000" + str(conn_key.loc[idx, 'ID'])
scores = pd.merge(scores, conn_key, how='right', on='ID')

#read chris scores
chris_scores = pd.read_excel("chris_scores.xls")
chris_scores = chris_scores[['Subj_ID', 'DMN_NF_DN']]

#renaming chris scores
chris_scores = chris_scores.rename(columns={'Subj_ID': 'ID'})
chris_scores = chris_scores.rename(columns={'DMN_NF_DN': 'chris_down'})

#merging chris scores with my scores
scores = pd.merge(scores, chris_scores, how='outer', on='ID')

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(scores[['ID', 'skourascore_down', 'chris_down']])
