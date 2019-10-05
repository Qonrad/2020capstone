import pandas as pd
import matplotlib.pyplot as plt
colors = ['red', 'blue', 'green', 'yellow', 'purple', 'black']
data = pd.read_csv("./out.tsv", sep="\t")
cols = data.columns.to_list()[2:]
rows = [data.skourascore_down, data.boxcarscore_down, data.skourascore_down_90, data.boxcarscore_down_90, data.areascore_down, data.areascore_down_90]
plt.hist(rows, stacked=False, color=colors, label=cols)
plt.legend()
plt.show()
