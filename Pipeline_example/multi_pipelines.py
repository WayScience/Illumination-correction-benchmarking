#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Modified Jenna's nf1_ic.ipynb file from the Cellpainting repo
# https://github.com/WayScience/nf1_cellpainting_data/blob/main/1.cellprofiler_ic/nf1_ic.ipynb

import pathlib
import pprint
import sys
sys.path.append("../scripts/")
import cp_parallel


# In[2]:


# set the run type for the parallelization
run_name = "illum_correction"

# set main output dir for all plates
output_dir = pathlib.Path("./Corrected_Images")
output_dir.mkdir(exist_ok=True)

# directory where pipelines are located 
pipelines_dir = pathlib.Path("/home/maggiekeating/Illumination-correction-benchmarking/Pipeline_example/Pipelines/")

# list for pipeline names based on files to use to create dictionary
pipeline_names = []

# iterate through "Pipelines" and append pipline_names from file names
for file_path in pathlib.Path("/home/maggiekeating/Illumination-correction-benchmarking/Pipeline_example/Pipelines/").iterdir():
    if str(file_path.stem).startswith("pipeline"):
        pipeline_names.append(str(file_path.stem))

plate_run_names = []

# iterate through "test" and append plate_run_names from folder name and corresponding pipeline name
for file_path in pathlib.Path("/home/maggiekeating/Illumination-correction-benchmarking/Pipeline_example/data/test_plate/").iterdir():
    if str(file_path.stem).startswith("Plate"):
        for i in range(len(pipeline_names)):
            plate_run_names.append(str(file_path.stem + "_" + pipeline_names[i]))

print(plate_run_names)


# In[3]:


# create plate info dictionary with all parts of the CellProfiler CLI command to run in parallel
plate_info_dictionary = {
    name: {    
        "path_to_images": pathlib.Path(f"../data/test_plate/Plate_1/"),
        "path_to_output": pathlib.Path(f"{output_dir}/Corrected_{name}"),
        }
        for name in plate_run_names
}
# iterate over the dictionary and add the path_to_pipeline 
for name, info in plate_info_dictionary.items():
        for i in range(len(plate_run_names)):
            if name == "Plate_1_" + pipeline_names[i]:
                info["path_to_pipeline"] = pathlib.Path(f"../Pipelines/" + pipeline_names[i]+ ".cppipe")

# view the dictionary to assess that all info is added correctly
pprint.pprint(plate_info_dictionary, indent=4)


# In[4]:


cp_parallel.run_cellprofiler_parallel(
    plate_info_dictionary=plate_info_dictionary, run_name=run_name
)

