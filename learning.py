from sklearn.feature_selection import SelectKBest, mutual_info_regression
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
#print(scores)
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if 'resultsROI' in file:
            files.append(os.path.join(r, file))
X = np.array([np.zeros((164 * 167) - 1)]) #quite possibly unnecessarily complicated, unsure how to do this
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
#print(X)
#print(X.shape)
#print(y.shape)

print("Imputing")
#imputing to remove NaN values using mean method
from sklearn.preprocessing import Imputer
imp = Imputer(missing_values='NaN', strategy='mean', axis=1)
X = imp.fit_transform(X)
#print(X)

num_features = 30
print("Running SelectKBest feature selection.")
print("Selecting", num_features, "features.")
#only using top 25 features
X_new = SelectKBest(mutual_info_regression, k=num_features).fit_transform(X, y)
print(X_new.shape)

from sklearn.svm import SVR
print("Attempting SVR")
clf = SVR(kernel='poly', gamma='scale', C=1.0, epsilon=0.2, verbose=True)
clf.fit(X_new, y)
print(clf.get_params())
print("R-squared =", clf.score(X_new, y))


print("attempting RidgeCV")
from sklearn.linear_model import RidgeCV
clf = RidgeCV(alphas=[1e-3, 1e-2, 1e-1, 1]).fit(X_new, y)
print(clf.coef_)
print(np.argwhere(clf.coef_ > 0.01))
print("R-squared =", clf.score(X_new, y))
print(clf.get_params())

print("Running LassoCV.")
from sklearn.linear_model import LassoCV
reg = LassoCV(cv=5, random_state=0, n_jobs=4).fit(X_new, y)
print(reg.get_params())
print("R-squared = ", reg.score(X_new, y))
print("alpha = ", reg.alpha_)
print("w =", reg.coef_)
