from sklearn.feature_selection import SelectKBest, mutual_info_regression
from scipy.io import loadmat
import os
import pandas as pd
import numpy as np
#/Users/Conrad/Box/Conrad Leonik Capstone/data/connectivity/connectivity_matrices/resultsROI_Subject002_Condition001.mat
"""
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
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
from sklearn.svm import SVR
from sklearn.pipeline import Pipeline

X = np.load("imputed_matrices.npy")
y = np.load("skourascores.npy")

#num_features = 30
#print("Running SelectKBest feature selection.")
#print("Selecting", num_features, "features.")
#only using top 25 features
#X = SelectKBest(mutual_info_regression, k=num_features).fit_transform(X, y)

# Split the dataset in two equal parts

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.15, random_state=0)

# Set the parameters by cross-validation
feats = len(X[0])
subs = len(y)

#tuned_parameters = [{'kernel': ['linear'], 'C': [0.0001, 0.001, 0.1, 1, 10, 100, 1000]}]

num_features = [feats, round(feats/subs) * 10, round(feats/subs), subs, 30]

pipe = Pipeline([
    # the reduce_dim stage is populated by the param_grid
    ('reduce_dim', SelectKBest(mutual_info_regression)),
    ('svr', SVR(verbose=10))
])

N_FEATURES_OPTIONS = ["all", round(feats/subs) * 10, round(feats/subs), subs, 30]
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

mean_scores = np.array(grid.cv_results_['mean_test_score'])
# scores are in the order of param_grid iteration, which is alphabetical
mean_scores = mean_scores.reshape(len(C_OPTIONS), -1, len(N_FEATURES_OPTIONS))
# select score for best C
mean_scores = mean_scores.max(axis=0)


#this is the part of the code I am most unsure about
#if there is a mysterious error, check these 2 lines
#sub_pipe = pipe[:1]
#y_selected = sub_pipe.transform(y_test)

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
print()

"""
for num in num_features:
    if num != None:
        print("Selecting", num, "features.")
        selection = SelectKBest(mutual_info_regression, k=num).fit(X_train, y_train)
        selected_training = selection.transform(X_train)
        selected_test = selection.transform(X_test)
    else:
        selected_training = X_train
        selected_test = X_test

    clf = GridSearchCV(SVR(), tuned_parameters, cv=5,
                       scoring='r2')
    clf.fit(selected_training, y_train)

    print("Best parameters set found on development set:")
    print()
    print(clf.best_params_)
    print()
    print("Grid scores on development set:")
    print()
    means = clf.cv_results_['mean_test_score']
    stds = clf.cv_results_['std_test_score']
    for mean, std, params in zip(means, stds, clf.cv_results_['params']):
        print("%0.3f (+/-%0.03f) for %r"
              % (mean, std * 2, params))
    print()

    print("Detailed classification report:")
    print()
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    print()
    y_true, y_pred = y_test, clf.predict(selected_test)
    print(r2_score(y_true, y_pred))
    print()
"""
