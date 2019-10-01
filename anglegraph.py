import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

trialOrders = {}

import os

path = '../../data/events'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.tsv' in file:
            files.append(os.path.join(r, file))

for i in range(len(files)):
    if i > 1:
        break
    data = pd.read_csv(files[i], sep="\t")
    #if data[data['instruction']!=" Rest"].instruction.tolist()[0] != " Focus": #skipping subjects that don't focus first
    #    continue
    #data[data['instruction']!=" Focus"].plot(kind='scatter', x='onset', y='needle_position')
    orig = data
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
        if data.loc[idx, 'left_text'] == " Focused": #if focused is on left, then switch it back
            data.loc[idx, 'needle_position'] = 180 - data.loc[idx, 'needle_position']
            data.loc[idx, 'left_text'] = " Wandering"
            data.loc[idx, 'right_text'] = " Focused"
        if data.loc[idx, 'instruction'] != " Focus": #remove data values on rows that don't have instruction == wander
            data.loc[idx, 'needle_position'] = None
    #data at this point is cleaned up and reversed (for uncounterbalancing)
    #calculating neurofeedback score for this subject
    #print(trialOrder)
    down_skourascores = []
    down_boxcarscores = []
    for trialnum in range(12):
        if trialOrder[(trialnum * 2) + 1] == "Focus":
            #print("Trial", trialnum, "had instruction == Focus")
            #this_trial is the data just from the trial of trialnum
            this_trial = data[(times[trialnum] + 1):times[trialnum + 1]][data['feedback']=="On"]
            #print(this_trial.needle_position.values)
            length = len(this_trial.needle_position.values)
            #print(length, "needle_position values")
            idealized = np.linspace(90, 90 - (length - 1), num=length)
            #print("Idealized needle_positions")
            #print(idealized)
            skourascore = scipy.stats.pearsonr(this_trial.needle_position.values, idealized)[0]
            down_skourascores += [skourascore]
            #print("Pearson’s correlation coefficient (Skouras score)=", skourascore)
            #print("\n")
            boxcar = np.full(length, 0)
            boxcar[0] = 90
            boxcar[-1] = 90
            #print(boxcar)
            boxcarscore = scipy.stats.pearsonr(this_trial.needle_position.values, boxcar)
            #print(boxcarscore)
            down_boxcarscores += [boxcarscore]
    #print(down_skourascores)
    subpos = files[i].find('sub-A')
    subjID = files[i][(subpos + 4):(subpos + 13)]
    print(subjID, np.mean(down_skourascores), np.mean(down_boxcarscores))
    #plt.plot(data.index, data['needle_position'], linewidth=0.75) #plots the graph similar to the figure
#plt.vlines(x=data[data['instruction']==" Push Button"].index.tolist(), ymin=0, ymax=180)
#plt.show()
