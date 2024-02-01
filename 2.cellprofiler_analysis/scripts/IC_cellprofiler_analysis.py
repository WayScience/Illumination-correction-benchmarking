#!/usr/bin/env python
# coding: utf-8

# # Perform segmentation and feature extraction for each plate using CellProfiler Parallel

# ## Import libraries

# In[1]:


# Modified Jenna's nf1_ic.ipynb file from the Cellpainting repo
# https://github.com/WayScience/nf1_cellpainting_data/blob/main/2.cellprofiler_analysis/nf1_analysis.ipynb

import sys

import pathlib
import pprint

sys.path.append("../../utils")
import cp_parallel


# ## Set paths and variables

# In[2]:


# set the run type for the parallelization
run_name = "analysis"

# set main output dir for all plates
output_dir = pathlib.Path("../outputs/SQLites")
output_dir.mkdir(exist_ok=True)

# directory where images are located within folders
images_dir = pathlib.Path("../../1.run_multi_IC_pipelines/data/test_plate/Plate_3_prime_sub")

# list for IC function names based on files to use to create dictionary
IC_function_names = []

# iterate through "IC_functions" and append IC_function_names from file names
for file_path in pathlib.Path("../../1.run_multi_IC_pipelines/data/test_plate/Plate_3_prime_sub/IC_functions/").iterdir():
    if str(file_path.stem).startswith("pipeline_"):
        IC_function_names.append(str(file_path.stem))

# iterate through "IC_function_names" and generate a pipeline that includes the correct IC functions for each 
for i in range(len(IC_function_names)):
    search_text = "IC_function_1"
    replace_text = IC_function_names[i] 

    with open("../pipelines/IC_function_apply_model.cppipe", 'r') as file:
        data = file.read()
        new_file = open('../pipelines/IC_function_apply_pipelines/' + IC_function_names[i] + '.cppipe', 'x')
        new_file.write(data)

    with open('../pipelines/IC_function_apply_pipelines/' + IC_function_names[i] + '.cppipe', 'r') as file:
        update = file.read()
        update = update.replace(search_text, replace_text)

    with open('../pipelines/IC_function_apply_pipelines/' + IC_function_names[i] + '.cppipe', 'w') as file: 
        file.write(update)

print(IC_function_names)


# ## Create dictionary with all info for each plate

# In[3]:


# create plate info dictionary with all parts of the CellProfiler CLI command to run in parallel
plate_info_dictionary = {
    name: {
        "path_to_images": pathlib.Path(f"../../1.run_multi_IC_pipelines/data/test_plate/Plate_3_prime_sub"),
        "path_to_output": pathlib.Path(f"{output_dir}"),
    }
    for name in IC_function_names
}

# iterate over the dictionary and add the path_to_pipeline 
for name, info in plate_info_dictionary.items():
        for i in range(len(IC_function_names)):
            if name == IC_function_names[i]:
                info["path_to_pipeline"] = pathlib.Path(f"../pipelines/IC_function_apply_pipelines/" + IC_function_names[i]+ ".cppipe")



# view the dictionary to assess that all info is added correctly
pprint.pprint(plate_info_dictionary, indent=4)


# ## Run analysis pipeline on each plate in parallel
# 
# This cell is not finished to completion due to how long it would take. It is ran in the python file instead.

# In[4]:


cp_parallel.run_cellprofiler_parallel(
    plate_info_dictionary=plate_info_dictionary, run_name=run_name
)

