
#%%
import subprocess
import openneuro as on
# create a dataset folder using makedirs
import os

#%% Step 1: initialize nipoppy
os.makedirs("dataset", exist_ok=True)

# Define the path to the dataset root
dataset_root_path = "/cubric/collab/487_mvpa/poppy-effex/dataset"  # Replace with the actual path 
# Define the command
command = ["nipoppy", "init", "--dataset-root", dataset_root_path]
# Execute the command
result = subprocess.run(command, capture_output=True, text=True, cwd="nipoppy")

# Print the output
print("stdout:", result.stdout)
print("stderr:", result.stderr)

#%% Step 2: Get sample subject data from an openneuro dataset that contains RS-fMRI and T1w images


# on.download(dataset='ds004965', include="sub-126BPCP021001/*(rest|T1w)*", target_dir = "bids_sample" )
# on.download(dataset='ds004965', include="sub-126BPCP021001/*", target_dir = "dataset/bids" ) # TODO: use fancy regex to download only the necessary files
on.download(dataset='ds004965', include="sub-126BPCP021002/*", target_dir = "dataset/bids" ) # TODO: use fancy regex to download only the necessary files


#%% Step 3: Generate a manifest file for nipoppy

import bids

# read the layout
layout = bids.BIDSLayout("dataset/bids")

import pandas as pd
from bids import BIDSLayout

# Extract the required fields
data = []
for subject in layout.get_subjects():
    for session in layout.get_sessions(subject=subject):
        datatype_list = []
        for datatype in layout.get_datatypes(subject=subject, session=session):
            # append datatype to empty list
            datatype_list = datatype_list + [datatype]
            # turn the list into a list of strings
            
        data.append({
            'participant_id': subject,
            'visit_id': session,
            'session_id': session,
            'datatype': str(datatype_list).replace('"', "'")
        })

# Create a DataFrame with the extracted data
df = pd.DataFrame(data)

# Print the DataFrame
# print(df)

# export the dataframe to a csv file
df.to_csv("dataset/manifest.csv", index=False)

#%% Step 4: Regenerate the dataset structure

# Define the command
command = ["nipoppy", "doughnut", "--dataset-root", dataset_root_path, "--regenerate"]

# Execute the command
result = subprocess.run(command, capture_output=True, text=True, cwd="nipoppy")

# Print the output
print("stdout:", result.stdout)
print("stderr:", result.stderr)
#%% Step 5: build preprocessing pipeline command

# Define the command
command = ["nipoppy", "run", "--dataset-root", dataset_root_path, "--pipeline", "fmriprep", "--pipeline-version", "20.2.7", "--participant-id", "126BPCP021002", "session-id", "1"]

# CLI command
# nipoppy run --dataset-root /cubric/collab/487_mvpa/poppy-effex/dataset --pipeline fmriprep
# nipoppy run --dataset-root /cubric/collab/487_mvpa/poppy-effex/dataset --pipeline fmriprep --pipeline-version 20.2.7 --participant-id 126BPCP021002

# Execute the command
result = subprocess.run(command, capture_output=True, text=True, cwd="nipoppy")

# Print the output
print("stdout:", result.stdout)
print("stderr:", result.stderr)
