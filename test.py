import pandas as pd
import numpy as np
scores = pd.read_csv("./out.tsv", sep="\t")
print(scores)
y = np.load("skourascores.npy")
print(y)
X = np.load("imputed_matrices.npy")
print(X[-2])
