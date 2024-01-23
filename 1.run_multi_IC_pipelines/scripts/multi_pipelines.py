#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Modified Jenna's nf1_ic.ipynb file from the Cellpainting repo
# https://github.com/WayScience/nf1_cellpainting_data/blob/main/1.cellprofiler_ic/nf1_ic.ipynb

import sys

import pathlib
import pprint

sys.path.append("../../utils")
import cp_parallel


# In[2]:


# set the run type for the parallelization
run_name = "illum_correction"

# set main output dir for all plates
output_dir = pathlib.Path("../outputs/npys_IC")
output_dir.mkdir(exist_ok=True)

# directory where pipelines are located 
pipelines_dir = pathlib.Path("../pipelines/")

# list for pipeline names based on files to use to create dictionary
pipeline_names = []

# iterate through "pipelines" and append pipline_names from file names
for file_path in pathlib.Path("../pipelines/").iterdir():
    if str(file_path.stem).startswith("pipeline"):
        pipeline_names.append(str(file_path.stem))

print(pipeline_names)


# In[3]:


# create plate info dictionary with all parts of the CellProfiler CLI command to run in parallel
plate_info_dictionary = {
    name: {    
        "path_to_images": pathlib.Path(f"../data/test_plate/Plate_3_prime_sub/"),
        "path_to_output": pathlib.Path(f"{output_dir}/{name}_IC"),
        }
        for name in pipeline_names
}
# iterate over the dictionary and add the path_to_pipeline 
for name, info in plate_info_dictionary.items():
    for i in range(len(pipeline_names)):
        if name == pipeline_names[i]:
            info["path_to_pipeline"] = pathlib.Path(f"../pipelines/{pipeline_names[i]}.cppipe")

# view the dictionary to assess that all info is added correctly
pprint.pprint(plate_info_dictionary, indent=4)


# In[4]:


cp_parallel.run_cellprofiler_parallel(
    plate_info_dictionary=plate_info_dictionary, run_name=run_name
)

