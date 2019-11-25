from shutil import copytree, ignore_patterns

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
#copytree("/Volumes/G-RAID/RAW/RawDataBIDS/sub-A00028185", "/Users/mac637-jbj-100/conrad/bids_subset_test/sub-A00028185")

def sieve(dir, contentslist):
    resultinglist = []
    for entry in contentslist:
        #print(entry)
        if ("." in entry) and ("DMNTRACKING" not in entry):
            resultinglist += [entry]
    return resultinglist

#create directories
for id in IDs:
    dirName = "/Users/mac637-jbj-100/conrad/bids_subset_test/" + "sub-" + id
    # Create target Directory if don't exist
    if not os.path.exists(dirName):
        #os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ")
        copytree(prefix + id, dirName, ignore=sieve)
    else:
        print("Directory " , dirName ,  " already exists")
