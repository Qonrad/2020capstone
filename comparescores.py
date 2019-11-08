import pandas as pd
import numpy as np

#read my scores
scores = pd.read_csv("./out.tsv", sep="\t")

#read chris scores
chris_scores = pd.read_excel("chris_scores.xls")
chris_scores = chris_scores[['Subj_ID', 'DMN_NF_DN', 'DMN_NF_90_DN']]

#renaming chris scores
chris_scores = chris_scores.rename(columns={'Subj_ID': 'ID'})
chris_scores = chris_scores.rename(columns={'DMN_NF_DN': 'chris_down'})
chris_scores = chris_scores.rename(columns={'DMN_NF_90_DN': 'chris_down_90'})

#merging chris scores with my scores
scores = pd.merge(scores, chris_scores, how='outer', on='ID')

#sorting scores by ID
scores = scores.sort_values('ID')

scores.to_csv("./out.tsv", sep="\t", index=False)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(scores[['ID', 'skourascore_down', 'chris_down']])
