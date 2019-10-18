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

X = np.load("imputed_matrices.npy")
y = np.load("skourascores.npy")

num_features = 80
print("Running SelectKBest feature selection.")
print("Selecting", num_features, "features.")
#only using top 25 features
X = SelectKBest(mutual_info_regression, k=num_features).fit_transform(X, y)

# Split the dataset in two equal parts
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.15, random_state=0)

# Set the parameters by cross-validation

tuned_parameters = [{'kernel': ['poly'], 'gamma': [1e-3, 1e-4],
                     'C': [1, 10, 100, 1000]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]

scores = ['explained_variance', 'max_error', 'r2']

for score in scores:
    print("# Tuning hyper-parameters for %s" % score)
    print()

    clf = GridSearchCV(SVR(), tuned_parameters, cv=5,
                       scoring=score)
    clf.fit(X_train, y_train)

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
    y_true, y_pred = y_test, clf.predict(X_test)
    print(r2_score(y_true, y_pred))
    print()


"""

print(X_new.shape)
"""

"""
from sklearn.svm import SVR
print("Attempting SVR")
clf = SVR(kernel='linear', gamma='scale', C=100.0, epsilon=0.2, verbose=True)
from sklearn.model_selection import cross_val_score
scores = cross_val_score(clf, X_train, y_train, cv=10)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


#print("R-squared =", clf.score(X_test, y_test))
"""
"""
print("attempting RidgeCV")
from sklearn.linear_model import RidgeCV
clf = RidgeCV(alphas=[1e-3, 1e-2, 1e-1, 1]).fit(X_train, y_train)
print(clf.coef_)
print(np.argwhere(clf.coef_ > 0.01))
print("R-squared =", clf.score(X_test, y_test))
print(clf.get_params())

print("Running LassoCV.")
from sklearn.linear_model import LassoCV
reg = LassoCV(cv=5, random_state=0, n_jobs=4).fit(X_train, y_train)
print(reg.get_params())
print("R-squared = ", reg.score(X_test, y_test))
print("alpha = ", reg.alpha_)
print("w =", reg.coef_)
"""
