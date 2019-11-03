from scipy.io import loadmat
import os
import pandas as pd
import numpy as np
path = './connectivity/connectivity_matrices'
scores = pd.read_csv("./out.tsv", sep="\t")
conn_key = pd.read_csv("./connectivity/conn_key")
files = []
#fixing subject IDs in conn_key
for idx, row in conn_key.iterrows():
    conn_key.loc[idx, 'ID'] = "A000" + str(conn_key.loc[idx, 'ID'])
#getting the subset of subjects with scores (only ones that also have connectivity matrices)
scores = pd.merge(scores, conn_key, how='right', on='ID')
#print(scores)
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if 'resultsROI' in file:
            files.append(os.path.join(r, file))
X = np.array([np.zeros((164 * 167))]) #quite possibly unnecessarily complicated, unsure how to do this
#it absolutely must be checked that the scores match up properly with the correct connectivity matrix
for i in range(len(files)):
    #print(files[i])
    #print(scores.ID.values[i])
    connectome = loadmat(files[i])
    #quite possibly unnecessarily complicated, unsure how to do this
    longarray = np.array([np.array(connectome['Z'].reshape(164 * 167).tolist())[1:]])
    #print(longarray)
    #print(X)
    X = np.concatenate((X, longarray), axis=0)
    #print(longarray)
y = scores.skourascore_down.values
#print(X.shape)
#print(y.shape)
X = X[1:] #removing zeros first element

subjnum = 1
print("Subject number", subjnum)
X = X[1:]
print(files[subjnum-1])
print(scores.ID.values[subjnum-1])
for i in range(len(X[subjnum-1])):
    print(i, X[subjnum-1][i])
    if i > 20:
        break

"""
np.save("skourascores", y)


#print(X)
#print(X.shape)
#print(y.shape)
print("Imputing")
#imputing to remove NaN values using mean method
from sklearn.preprocessing import Imputer
imp = Imputer(missing_values='NaN', strategy='mean', axis=1)
X = imp.fit_transform(X)
np.save("imputed_matrices", X)
exit()
#print(X)
"""