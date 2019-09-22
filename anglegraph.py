import pandas as pd
import matplotlib.pyplot as plt

trialOrders = {}

import os

path = '/Users/Conrad/research/events'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.tsv' in file:
            files.append(os.path.join(r, file))

for i in range(len(files)):
    #print(f)
    if i > 50:
        break
    data = pd.read_csv(files[i], sep="\t")
    #data[data['instruction']!=" Focus"].plot(kind='scatter', x='onset', y='needle_position')
    orig = data
    intermissions = data[data['instruction']==" Push Button"].index.tolist()
    rests = data[data['instruction']==" Rest"]
    first_scan_index = data[data['instruction']!=" Rest"].index.tolist()[0] - 1
    first_rest_at_end = data[data['instruction']!=" Rest"].index.tolist()[-1] + 1
    times = [first_scan_index] + intermissions + [first_rest_at_end]
    trialOrder = []
    for trialnum in range(12):
        trialimes = (times[trialnum] + 1, times[trialnum + 1])
        #print("Trial", trialnum + 1)
        this_trial = data[(times[trialnum] + 1):times[trialnum + 1]][data['feedback']=="On"]
        trialOrder += [this_trial['left_text'].tolist()[0][1:] + "-" + this_trial['right_text'].tolist()[0][1:], this_trial['instruction'].tolist()[0][1:]]
        """
        if this_trial['left_text'].tolist()[0][1:] == "Wandering":
            print("Wandering")
        else: #multiply by -1 if left_text=="Focused"
            this_trial['needle_position'] = this_trial['needle_position'].apply(lambda x: x*-1)
            print("Focused")
        """
    #print(data)
    for idx, row in data.iterrows():
        if data.loc[idx, 'left_text'] == " Focused": #if focused is on left, then switch it back
            data.loc[idx, 'needle_position'] = 180 - data.loc[idx, 'needle_position']
            data.loc[idx, 'left_text'] = " Wandering"
            data.loc[idx, 'right_text'] = " Focused"
        if data.loc[idx, 'instruction'] != " Focus":
            data.loc[idx, 'needle_position'] = None
    plt.plot(data['onset'], data['needle_position'])
    #with pd.option_context('display.max_rows', None):  # more options can be specified also
    #    print(data)
    #data[data['instruction']!=" Focus"].plot(kind='line', x='onset', y='needle_position')
plt.vlines(x=data[data['instruction']==" Push Button"].onset.tolist(), ymin=0, ymax=180)
plt.show()
#print(trialOrder)
#remianing steps
#reverse angle measurement appropriately
#color graph
#scale up to work with all subjects
#graph all subjects
#???
#profit
