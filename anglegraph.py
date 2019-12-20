import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

trialOrders = {}

import os

path = './events'


def skourascore():
    return

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.tsv' in file:
            files.append(os.path.join(r, file))

outputdict = {'ID':[], 'skourascore_down': [], 'skourascore_down_90': []}

for i in range(len(files)):
    #parsing filename to find NKI subject ID
    subpos = files[i].find('sub-A')
    subjID = files[i][(subpos + 4):(subpos + 13)]
    print(subjID)
    data = pd.read_csv(files[i], sep="\t")
    #if data[data['instruction']!=" Rest"].instruction.tolist()[0] != " Focus": #skipping subjects that don't focus first
    #    continue
    #data[data['instruction']!=" Focus"].plot(kind='scatter', x='onset', y='needle_position')
    intermissions = data[data['instruction']==" Push Button"].index.tolist()
    rests = data[data['instruction']==" Rest"]
    first_scan_index = data[data['instruction']!=" Rest"].index.tolist()[0] - 1
    first_rest_at_end = data[data['instruction']!=" Rest"].index.tolist()[-1] + 1
    times = [first_scan_index] + intermissions + [first_rest_at_end]
    trialOrder = []
    for trialnum in range(12):
        this_trial = data[(times[trialnum] + 1):times[trialnum + 1]][data['feedback']=="On"]
        trialOrder += [this_trial['left_text'].tolist()[0][1:] + "-" + this_trial['right_text'].tolist()[0][1:], this_trial['instruction'].tolist()[0][1:]]
    #correcting needle_positions for the counterbalanced polarity
    for idx, row in data.iterrows():
        if data.loc[idx, 'instruction'] != " Focus": #remove data values on rows where they are told to wander
            data.loc[idx, 'needle_position'] = None
    #data at this point is cleaned up and reversed (for uncounterbalancing)
    #calculating neurofeedback score for this subject
    down_skourascores = []
    down_skourascores_90 = []
    print(trialOrder)
    print(times)
    for trialnum in range(12):
        if trialOrder[(trialnum * 2) + 1] == "Focus":
            #this_trial is the data just from the trial of trialnum
            this_trial = data[(times[trialnum] + 1):times[trialnum + 1]]#[data['feedback']=="On"]
            length = len(this_trial.needle_position.values)
            print("Trial", trialnum + 1, "was", (length-1)*2, "seconds long and contained", length, "needle_position values.")
            print("needle_position values")
            print(this_trial.needle_position.values)
            print(trialOrder[(trialnum * 2)])
            if trialOrder[(trialnum * 2)] == 'Focused-Wandering':
                idealized = np.linspace(90, 90 + (length - 1), num=length)
                print("Idealized needle_positions")
                print(idealized)
            elif trialOrder[(trialnum * 2)] == 'Wandering-Focused':
                idealized = np.linspace(90, 90 - (length - 1), num=length)
                print("Idealized needle_positions")
                print(idealized)
            skourascore = scipy.stats.pearsonr(this_trial.needle_position.values, idealized)[0]
            print("Score for this trial:", skourascore)
            down_skourascores += [skourascore]
            if length == 46:
                down_skourascores_90 += [skourascore]
    print(down_skourascores)
    outputdict['ID'] += [subjID]
    outputdict['skourascore_down'] += [np.mean(down_skourascores)]
    outputdict['skourascore_down_90'] += [np.mean(down_skourascores_90)]

    print(subjID, np.mean(down_skourascores))
df = pd.DataFrame(outputdict)
df = df.sort_values(by=['ID'])
print(df)
df.to_csv("./newout.tsv", sep="\t", index=False)
