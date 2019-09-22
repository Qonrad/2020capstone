import pandas as pd
import matplotlib.pyplot as plt

trialOrders = {}

data = pd.read_csv("/Users/Conrad/research/events/sub-A00028185_ses-NFB3_task-DMNTRACKINGTEST_events.tsv", sep="\t")
#data.plot(kind='line', y='needle_position')
intermissions = data[data['instruction']==" Push Button"].index.tolist()
rests = data[data['instruction']==" Rest"]
first_scan_index = data[data['instruction']!=" Rest"].index.tolist()[0] - 1
first_rest_at_end = data[data['instruction']!=" Rest"].index.tolist()[-1] + 1
times = [first_scan_index] + intermissions + [first_rest_at_end]
trialOrder = []
for trialnum in range(12):
    trialimes = (times[trialnum] + 1, times[trialnum + 1])
    print("Trial", trialnum + 1)
    this_trial = data[(times[trialnum] + 1):times[trialnum + 1]][data['feedback']=="On"]
    trialOrder += [this_trial['left_text'].tolist()[0][1:] + "-" + this_trial['right_text'].tolist()[0][1:], this_trial['instruction'].tolist()[0][1:]]
#plt.show()
print(trialOrder)
