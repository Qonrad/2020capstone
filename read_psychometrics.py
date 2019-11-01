import pandas as pd

pmetrics = pd.read_excel("./NKI-merged demographic and assessment data_5.28.19.xlsx", sheet_name='NeuropsychTesting')
all = pd.DataFrame()
scores = pd.read_csv("./out.tsv", sep="\t")
feats = pd.read_csv("Neuropsych_features.txt")
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
