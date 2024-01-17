#!/usr/bin/env python
# coding: utf-8

# ## Perform traditional bulk pycytominer pipeline
# 
# Following single-cell curation with cytotable, we create bulk profiles by applying the following steps:
# 
# 1. aggregation
# 2. annotation
# 3. normalization
# 4. feature_selection

# In[1]:


# Modified Jenna's nf1_ic.ipynb file from the Cellpainting repo
# https://github.com/WayScience/nf1_cellpainting_data/blob/main/3.processing_features/2.pycytominer_singlecell_pipelines.ipynb

import pathlib
import yaml
import pprint

import pandas as pd

from pycytominer import aggregate, annotate, normalize, feature_select
from pycytominer.cyto_utils import load_profiles


# In[2]:


# Set constants
feature_select_ops = [
    "variance_threshold",
    "correlation_threshold",
    "blocklist",
]

# Set paths
output_dir = pathlib.Path("../outputs/bulk_profiles")
output_dir.mkdir(exist_ok=True)
metadata_dir = pathlib.Path("../../1.run_multi_IC_pipelines/data/Metadata/platemap_NF1_plate3_sub.csv")

# load in plate information
dictionary_path = pathlib.Path("../outputs/plate_info_dictionary.yaml")
with open(dictionary_path) as file:
    plate_info_dictionary = yaml.load(file, Loader=yaml.FullLoader)


# In[3]:


# add path to platemaps for each plate 
for plate in plate_info_dictionary.keys():
    plate_info_dictionary[plate]["platemap_path"] = str(pathlib.Path(metadata_dir))

# view the dictionary to assess that all info is added correctly
pprint.pprint(plate_info_dictionary, indent=4)


# ## Perform pycytominer pipeline

# In[4]:


for plate, info in plate_info_dictionary.items():
    print(f"Now performing pycytominer pipeline for {plate}")
    output_aggregated_file = str(pathlib.Path(f"{output_dir}/{plate}_bulk.parquet"))
    output_annotated_file = str(pathlib.Path(f"{output_dir}/{plate}_bulk_annotated.parquet"))
    output_normalized_file = str(pathlib.Path(f"{output_dir}/{plate}_bulk_normalized.parquet"))
    output_feature_select_file = str(pathlib.Path(f"{output_dir}/{plate}_bulk_feature_selected.parquet"))
    
    # Load single-cell profiles
    single_cell_df = pd.read_parquet(info["dest_path"])
    
    # Load platemap
    platemap_df = pd.read_csv(info["platemap_path"])

    # Step 1: Aggregation
    aggregate(
        population_df=single_cell_df,
        operation="median",
        strata=["Image_Metadata_Plate", "Image_Metadata_Well"],
        output_file=output_aggregated_file,
        output_type="parquet"
    )
    
    # Step 2: Annotation
    annotate(
        profiles=output_aggregated_file,
        platemap=platemap_df,
        join_on=["Metadata_well_position", "Image_Metadata_Well"],
        output_file=output_annotated_file,
        output_type="parquet",
    )
    
    # Step 3: Normalization
    normalized_df = normalize(
        profiles=output_annotated_file,
        method="standardize",
        output_file=output_normalized_file,
        output_type="parquet",
    )
    
    # Step 4: Feature selection
    feature_select(
        output_normalized_file,
        operation=feature_select_ops,
        output_file=output_feature_select_file,
        output_type="parquet"
    )


# In[5]:


# Check output file
test_df = load_profiles(output_feature_select_file)

print(test_df.shape)
test_df.head(2)

