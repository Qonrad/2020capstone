import pandas as pd
import matplotlib.pyplot as plt

ax = plt.gca()

data = pd.read_csv("/Users/Conrad/research/events/sub-A00028185_ses-NFB3_task-DMNTRACKINGTEST_events.tsv", sep="\t")
data.plot(kind='line', y='needle_position', ax=ax)
plt.show()
