from sklearn.feature_selection import SelectKBest, mutual_info_regression
from scipy.io import loadmat
from scipy.stats import pearsonr, spearmanr
import os
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
from sklearn.svm import SVR
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

#reading scores and filtering them by the conn_key
conn_key = pd.read_csv("./connectivity/conn_key")
for idx, row in conn_key.iterrows():
    conn_key.loc[idx, 'ID'] = "A000" + str(conn_key.loc[idx, 'ID'])
scores = pd.read_csv("./out.tsv", sep="\t")
scores = pd.merge(scores, conn_key, how='right', on='ID')
y = scores.skourascore_down.values

#read ages and filter them by IDs in scores
ages = pd.read_csv("ages.csv")
ages = pd.merge(scores['ID'], ages, how='left', on='ID')
ages = ages.AGE.values
ages = ages.reshape(-1,1)

#read chris_feats, filter only ones in conn_key, and drop columns with missing data
chris_feats = pd.read_csv("chris_feats.csv")
chris_feats = pd.merge(chris_feats, conn_key, how='right', on='ID')
chris_feats = chris_feats.dropna(axis='columns')

#extract binary features and encode them
chris_bools = chris_feats[['Sex', 'Clinical_Status', 'DEM_003']]
chris_bools = chris_bools.values
enc = OneHotEncoder(handle_unknown='ignore')
chris_bools = enc.fit_transform(chris_bools).toarray()

#extract non-binary features
chris_nonbools = chris_feats.drop(columns=['ID', 'Sex', 'Clinical_Status', 'DEM_003']).values

#read connectomes and add ages and chris_nonbools
X = np.load("connectomes.npy")
X = np.concatenate((ages, X), axis=1)
X = np.concatenate((chris_nonbools, X), axis=1)

#scaling features
scaler = preprocessing.StandardScaler().fit(X)
X = scaler.transform(X)

#add chris_bools
X = np.concatenate((chris_bools, X), axis=1)

# Split the dataset in two parts
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.15)

# Set the parameters by cross-validation
feats = len(X[0])
subs = len(y)
num_features = [feats, round(feats/subs) * 10, round(feats/subs), subs, 30]

pipe = Pipeline([
    # the reduce_dim stage is populated by the param_grid
    ('reduce_dim', SelectKBest(mutual_info_regression)),
    ('svr', SVR(verbose=10))
])

N_FEATURES_OPTIONS = [30, "all", round(feats/subs) * 10, round(feats/subs), subs]
C_OPTIONS = [0.0001, 0.001, 0.1, 1, 10, 100, 1000]
param_grid = [
    {
        'reduce_dim__k': N_FEATURES_OPTIONS,
        'svr__kernel': ['linear'],
        'svr__C': C_OPTIONS
    }
]

grid = GridSearchCV(pipe, cv=5, n_jobs=-1, param_grid=param_grid, iid=False, verbose=10)
grid.fit(X_train, y_train)

print("Best parameters set found on development set:")
print()
print(grid.best_params_)
print()
print("Grid scores on development set:")
print()
means = grid.cv_results_['mean_test_score']
stds = grid.cv_results_['std_test_score']
for mean, std, params in zip(means, stds, grid.cv_results_['params']):
    print("%0.3f (+/-%0.03f) for %r"
          % (mean, std * 2, params))
print()

print("Detailed classification report:")
print()
print("The model is trained on", len(y_train), "subjects.")
print("The scores are computed on", len(y_test), "subjects.")
print()
y_true, y_pred = y_test, grid.predict(X_test)
print(r2_score(y_true, y_pred))
