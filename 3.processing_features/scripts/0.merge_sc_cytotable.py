#!/usr/bin/env python
# coding: utf-8

# # Merge single cells from CellProfiler outputs using CytoTable

# ## Import libraries

# In[1]:


# Modified Jenna's nf1_ic.ipynb file from the Cellpainting repo
# https://github.com/WayScience/nf1_cellpainting_data/blob/main/3.processing_features/0.merge_sc_cytotable.ipynb

import pprint
import sys

# cytotable will merge objects from SQLite file into single cells and save as parquet file
from cytotable import convert, presets
import pandas as pd
import pathlib
import yaml

# import utility to use function that will add single-cell count per well as a metadata column
sys.path.append("../../utils/")
import extraction_utils as sc_utils


# ## Set paths and variables

# In[2]:


# type of file output from CytoTable (currently only parquet)
dest_datatype = "parquet"

# preset configurations based on typical CellProfiler outputs
preset = "cellprofiler_sqlite_pycytominer"

# update preset to include site metadata and cell counts
joins = presets.config["cellprofiler_sqlite_pycytominer"]["CONFIG_JOINS"].replace(
    "Image_Metadata_Well,",
    "Image_Metadata_Well, Image_Metadata_Site,",
)

# set main output dir for all parquet files
output_dir = pathlib.Path("../outputs/converted_data/")
output_dir.mkdir(exist_ok=True)

# directory where SQLite files are located
sqlite_dir = pathlib.Path("../../2.cellprofiler_analysis/outputs/SQLites/")

# list for pipeline names based on files to use to create dictionary
pipeline_names = []

# iterate through "IC_function_apply_pipelines" and append pipline_names from file names
for file_path in pathlib.Path("../../2.cellprofiler_analysis/pipelines/IC_function_apply_pipelines").iterdir():
    if str(file_path.stem).startswith("IC_function"):
        pipeline_names.append(str(file_path.stem))

print(pipeline_names)


# ## Create dictionary with info for each plate
# 
# **Note:** All paths must be string to use with CytoTable.

# In[3]:


# create plate info dictionary with all parts of the CellProfiler CLI command to run in parallel
plate_info_dictionary = {
    name: {
        "dest_path": str(pathlib.Path(f"{output_dir}/{name}.parquet")),
    }
    for name in pipeline_names 
}

# iterate over the dictionary and add the source_path
for name, info in plate_info_dictionary.items():
    for i in range(len(pipeline_names)):
        if name == pipeline_names[i]:
            info["source_path"] = str(pathlib.Path(f"../../2.cellprofiler_analysis/outputs/SQLites/{pipeline_names[i]}.sqlite"))

# view the dictionary to assess that all info is added correctly
pprint.pprint(plate_info_dictionary, indent=4)


# ## Merge objects to single cells and convert SQLite to parquet file + add single cell metadata

# In[4]:


# run through each run with each set of paths based on dictionary
for plate, info in plate_info_dictionary.items():
    source_path = info["source_path"]
    dest_path = info["dest_path"]
    
    print(f"Performing merge single cells and conversion on {plate}!")

    # merge single cells and output as parquet file
    convert(
        source_path=source_path,
        dest_path=dest_path,
        dest_datatype=dest_datatype,
        preset=preset,
        joins=joins,
    )
    print(f"Merged and converted {pathlib.Path(dest_path).name}!")

    # add single cell count per well as metadata column to parquet file and save back to same path
    sc_utils.add_sc_count_metadata_file(
        data_path=dest_path, well_column_name="Image_Metadata_Well", file_type="parquet"
    )

    # Remove NAs from ImageNumber column (artifact from Cytotable)
    df = pd.read_parquet(dest_path)
    df = df.dropna(subset=["Metadata_ImageNumber"])
    df.to_parquet(dest_path, index=False)
    
    print(f"Added single cell count as metadata and removed NAN ImageNumber rows to {pathlib.Path(dest_path).name}!")


# ### Check if converted data looks correct

# In[5]:


converted_df = pd.read_parquet(plate_info_dictionary["IC_function_1"]["dest_path"])

print(converted_df.shape)
converted_df.head()


# ## Write dictionary to yaml file for use in downstream steps

# In[ ]:


dictionary_path = pathlib.Path("../outputs/plate_info_dictionary.yaml")
with open(dictionary_path, 'w') as file:
    yaml.dump(plate_info_dictionary, file)

