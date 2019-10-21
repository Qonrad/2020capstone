import pandas as pd

pmetrics = pd.read_excel("./NKI-merged demographic and assessment data_5.28.19.xlsx", sheet_name=None)
all = pd.DataFrame()
scores = pd.read_csv("./out.tsv", sep="\t")
feats = pd.read_csv("Neuropsych_features.txt")
feat_cols = ['ID']
for k in pmetrics.keys():
    sht = pmetrics[k]
    #drop complete duplicates
    sht = sht.drop_duplicates()
    #adjust ID column name
    sht = sht.rename(columns={'Unnamed: 0': 'ID'})
    #adjust column names
    temp = sht.columns
    for col in temp:
        if 'Unnamed:' in col:
            if pd.notna(sht[col][0]):
                sht = sht.rename(columns={col: sht[col][0]})
    for c in sht.columns:
        for f in feats['Feature']:
            print(sht[c][0:10])
            if f in sht[c][0:10]:
                feat_cols += [c]
    #select only rows for subjects that we have scores for
    sht = pd.merge(scores['ID'], sht, how='left', on='ID')
    #merge those rows onto the running dataframe
    if all.empty:
        all = sht
    else:
        all = pd.merge(all, sht, how='left', on='ID')
    #print(all['ID'])
all = all.drop_duplicates(subset='ID') #when there's a duplicate ID, taking the first row with that ID
print(feat_cols)
all[feat_cols].to_csv("full_subset.csv")