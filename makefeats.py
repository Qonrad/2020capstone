from scipy.io import loadmat
import os
import pandas as pd
import numpy as np

"""
reads connectivity matrices
It reads all available files in numerical order.
returns numpy array formatted for sklearn
"""
def read_connectivity(mats_path):
    path = mats
    files = []

    # puts a list of individual filepaths into the files variable
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if 'resultsROI' in file:
                files.append(os.path.join(r, file))

    #create an array of the correct dimension to append to
    #first element is a placeholder full of 13366 0s
    X = np.array([np.zeros(13366)])

    #go through all of the files and add the non-redundant parts of the connectivity matrix to X
    for i in range(len(files)):
        #set mat to just the matrix (ignoring the last 3 grey-matter variables)
        mat = loadmat(files[i])['Z']
        mat = mat[:,0:len(mat[0]) - 3]

        #create a variable (brief) to store the non-redundant (only top-right) sections of the matrix
        brief = np.array([])
        for j in range(len(mat)):
            brief = np.concatenate((brief, mat[j][j+1:]), axis=0)

        #encapsulate brief in a temporary outer array, so that it can be appended to X (it needs to have the same shape)
        temp = np.array([brief.tolist()])
        X = np.concatenate((X, temp), axis=0)

    #return filtered connectivity matrix without the placeholder of 0s
    return X[1:]
mats = './connectivity/connectivity_matrices'

def convert_to_ROI_name(n, nonred_mat_position):
    #print(nonred_mat_position)
    pos_counter = 0
    for row in range(164):
        for col in range(row + 1, 164):
            #print(col, pos_counter, n[col][0])
            if pos_counter == nonred_mat_position:
                return "source: " + n[row][0] + " target: " + n[col][0]
            pos_counter += 1
    return "either this is a bug or the number given was out of range"



def convert_support(sup, extralen, matatend=True):
    if matatend:
        names = loadmat('./connectivity/connectivity_matrices/resultsROI_Subject001_Condition001.mat')['names']
        for s in sup:
            if s > extralen:
                print(s, "is the connectivity between", convert_to_ROI_name(names[0], s - extralen))
            else:
                print(s, "is not part of the connectivity matrix")

convert_support([13366], 1)
#print(read_connectivity(mats))
#print(np.load("connectomes.npy"))
