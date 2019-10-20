import pandas as pd
"""
pmetrics = pd.read_excel("./NKI-merged demographic and assessment data_5.28.19.xlsx", sheet_name=None)
all = pd.DataFrame()
scores = pd.read_csv("./out.tsv", sep="\t")
for k in pmetrics.keys():
    sht = pmetrics[k]
    sht = sht.drop_duplicates()
    sht = sht.rename(columns={'Unnamed: 0': 'ID'})
    temp = sht.columns
    for col in temp:
        if 'Unnamed:' in col:
            sht = sht.rename(columns={col: sht[col][0]})
    sht = pd.merge(scores['ID'], sht, how='left', on='ID')
    print(k)
    print(sht['ID'].to_list())
    if all.empty:
        all = sht
    else:
        all = pd.merge(all, sht, how='left', on='ID')
    #print(all['ID'])
all = all.drop_duplicates(subset='ID') #when there's a duplicate, taking the first row with that ID
all.to_csv("pmetrics.csv")
"""
all = pd.read_csv("pmetrics.csv")
