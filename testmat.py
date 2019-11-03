from scipy.io import loadmat
import os
import pandas as pd
import numpy as np
#/Users/Conrad/Box/Conrad Leonik Capstone/data/connectivity/connectivity_matrices/resultsROI_Subject002_Condition001.mat
path = './connectivity/connectivity_matrices'
scores = pd.read_csv("./out.tsv", sep="\t")
conn_key = pd.read_csv("./connectivity/conn_key")
files = []
#fixing subject IDs in conn_key
for idx, row in conn_key.iterrows():
    conn_key.loc[idx, 'ID'] = "A000" + str(conn_key.loc[idx, 'ID'])
#getting the subset of subjects with scores (only ones that also have connectivity matrices)
scores = pd.merge(scores, conn_key, how='right', on='ID')
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if 'resultsROI' in file:
            files.append(os.path.join(r, file))
X = np.array([np.zeros(13366)]) #quite possibly unnecessarily complicated, unsure how to do this
#it absolutely must be checked that the scores match up properly with the correct connectivity matrix

for i in range(len(files)):
    connectome = loadmat(files[i])
    mat = connectome['Z']
    mat = mat[:,0:len(mat[0]) - 3]
    brief = np.array([])
    for j in range(len(mat)):
        #print(mat[j][j+1:])
        brief = np.concatenate((brief, mat[j][j+1:]), axis=0)
    #print(brief)
    temp = np.array([brief.tolist()])
    X = np.concatenate((X, temp), axis=0)
X = X[1:]
np.save("connectomes", X)
subjnum = 85
print("Subject number", subjnum)

print(files[subjnum-1])
print(scores.ID.values[subjnum-1])
for i in range(len(X[subjnum-1])):
    print(i, X[subjnum-1][i])
    if i > 20:
        break
y = scores.skourascore_down.values
