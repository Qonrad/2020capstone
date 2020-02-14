from shutil import copytree, ignore_patterns, copy2

import os

counter = 0
IDs = []
prefix = "/Volumes/G-RAID/RAW/RawDataBIDS/sub-"
for root, dirs, files in os.walk("/Volumes/G-RAID/RAW/RawDataBIDS"):
    for file in files:
        if ("DMNTRACKING" in file):
            print(os.path.join(root, file))
            fullpath = "/".join(root.split("/")[0:-2])
            print(fullpath)
            id = fullpath[-9:]
            print(id)
            if not id.startswith("A"):
                continue
            if id not in IDs:
                IDs += ["/".join(root.split("/")[0:-2])[-9:]]
                counter += 1
print("total", counter, "files (with unique sub-IDs) matching the string in the code")
print(IDs)

def sieve(dir, contentslist):
    return []

odirName = "/Volumes/G-RAID/nfb_subset/"
#copy specific other files necessary for bids
addl_bids_files = ["/Volumes/G-RAID/RAW/RawDataBIDS/dataset_description.json",
"/Volumes/G-RAID/RAW/RawDataBIDS/T1w.json",
"/Volumes/G-RAID/RAW/RawDataBIDS/task-DMNTRACKINGTEST_bold.json",
"/Volumes/G-RAID/RAW/RawDataBIDS/task-DMNTRACKINGTRAIN_bold.json",
"/Volumes/G-RAID/RAW/RawDataBIDS/participants.tsv",
"/Volumes/G-RAID/RAW/RawDataBIDS/README"]

for f in addl_bids_files:
    copy2(f, odirName)

#create directories
for id in IDs:
    dirName = odirName + "sub-" + id
    # Create target Directory if don't exist
    if not os.path.exists(dirName):
        #os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ")
        copytree(prefix + id, dirName, ignore=sieve)
    else:
        print("Directory " , dirName ,  " already exists")


for root, dirs, files in os.walk("/Volumes/G-RAID/nfb_subset/"):
    for file in files:
        if ("DMNTRACKINGTRAIN" in file):
            fullpath = os.path.join(root, file)
            rev_file = file[0:file.find("task-")] + "task-" + "rest" + file[(file.find("task-") + 5):]
            rev_fullpath = os.path.join(root, rev_file)
            os.rename(fullpath, rev_fullpath)
            print(fullpath)
            print(rev_fullpath)
