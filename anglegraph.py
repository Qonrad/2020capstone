import pandas as pd
import numpy as np
import scipy.stats

trialOrders = {}

import os

path = './events'


def compute_skourascore(subject_performace, idealized_performance):
    return scipy.stats.pearsonr(subject_performace, idealized_performance)[0]


def find_empty_times(data):
    intermissions = data[data['instruction']==" Push Button"].index.tolist()
    rests = data[data['instruction']==" Rest"]
    first_scan_index = data[data['instruction']!=" Rest"].index.tolist()[0] - 1
    first_rest_at_end = data[data['instruction']!=" Rest"].index.tolist()[-1] + 1
    times = [first_scan_index] + intermissions + [first_rest_at_end]
    return times

def determine_trialorder(data, times):
    trialOrder = []
    for trialnum in range(12):
        this_trial = data[(times[trialnum] + 1):times[trialnum + 1]][data['feedback']=="On"]
        trialOrder += [this_trial['left_text'].tolist()[0][1:] + "-" + this_trial['right_text'].tolist()[0][1:], this_trial['instruction'].tolist()[0][1:]]
    return trialOrder

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.tsv' in file:
            files.append(os.path.join(r, file))

outputdict = {'ID':[], 'skourascore_down': [], 'skourascore_down_90': [], 'skourascore_up': [], 'skourascore_up_90': [], 'skourascore_both': [], 'skourascore_both_90': []}

for i in range(len(files)):
    #parsing filename to find NKI subject ID
    subpos = files[i].find('sub-A')
    subjID = files[i][(subpos + 4):(subpos + 13)]
    print(subjID)
    #reading events.tsv file as "data"
    data = pd.read_csv(files[i], sep="\t")
    times = find_empty_times(data)
    trialOrder = determine_trialorder(data, times)
    down_skourascores = []
    down_skourascores_90 = []
    up_skourascores = []
    up_skourascores_90 = []
    both_skourascores = []
    both_skourascores_90 = []
    for trialnum in range(12):
        #this_trial is the data just from the trial of trialnum
        this_trial = data[(times[trialnum] + 1):times[trialnum + 1]]
        length = len(this_trial.needle_position.values)
        #print("Trial", trialnum + 1, "was", (length-1)*2, "seconds long and contained", length, "needle_position values.")
        #print("needle_position values")
        #print(this_trial.needle_position.values)
        #print(trialOrder[(trialnum * 2)])
        if trialOrder[(trialnum * 2) + 1] == "Focus":
            if trialOrder[(trialnum * 2)] == 'Focused-Wandering':
                idealized = np.linspace(90, 90 + (length - 1), num=length)
            elif trialOrder[(trialnum * 2)] == 'Wandering-Focused':
                idealized = np.linspace(90, 90 - (length - 1), num=length)
            skourascore = compute_skourascore(this_trial.needle_position.values, idealized)
            down_skourascores += [skourascore]
            if length == 46:
                down_skourascores_90 += [skourascore]
        elif trialOrder[(trialnum * 2) + 1] == "Wander":
            if trialOrder[(trialnum * 2)] == 'Focused-Wandering':
                idealized = np.linspace(90, 90 - (length - 1), num=length)
            elif trialOrder[(trialnum * 2)] == 'Wandering-Focused':
                idealized = np.linspace(90, 90 + (length - 1), num=length)
            skourascore = compute_skourascore(this_trial.needle_position.values, idealized)
            up_skourascores += [skourascore]
            if length == 46:
                up_skourascores_90 += [skourascore]
        else:
            print("something is horribly wrong")
        both_skourascores += [skourascore]
        if length == 46:
            both_skourascores_90 += [skourascore]
    #print(down_skourascores)
    outputdict['ID'] += [subjID]
    outputdict['skourascore_down'] += [np.mean(down_skourascores)]
    outputdict['skourascore_down_90'] += [np.mean(down_skourascores_90)]
    outputdict['skourascore_up'] += [np.mean(up_skourascores)]
    outputdict['skourascore_up_90'] += [np.mean(up_skourascores_90)]
    outputdict['skourascore_both'] += [np.mean(both_skourascores)]
    outputdict['skourascore_both_90'] += [np.mean(both_skourascores_90)]
    #print(subjID, np.mean(down_skourascores))
df = pd.DataFrame(outputdict)
df = df.sort_values(by=['ID'])
print(df)
df.to_csv("./newout.tsv", sep="\t", index=False)
