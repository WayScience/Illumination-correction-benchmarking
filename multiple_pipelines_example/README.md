# Perform illumination correction using multiple pipelines
In this module, we perform illumination correction (IC) on a single set of images using multiple CellProfiler pipelines. As this is an intermediate step in our image processing, the corrected images will not be saved. Instead, the npy files for each channel will be saved in a new folder. 

## Download images
Images utilized in this module were downloaded from the [NF1 Schwann Cell Genotype Cell Painting Assay folder](https://figshare.com/projects/NF1_Schwann_Cell_Genotype_Cell_Painting_Assay/161620)  on [Figshare](https://figshare.com/). A subset of images (B1-B4) from Plate 3' were used. Instructions for how to download the images can be found on our [nf1_cellpainting_data repository](https://github.com/WayScience/nf1_cellpainting_data/tree/main/0.download_data), courtesy of Jenna Tomkinson. 

## CellProfiler Pipelines 
The goal of this repository is to evaluate the performance of different IC parameters by utilizing multiple CellProfiler pipelines. An overview of CellProfiler IC parameters can be found at Jenna Tomkinson's [Steps for Performing Illumination Correction in Microscopy Images](https://www.waysciencelab.com/2023/08/07/illumsteps.html) blog. 

>[!Note]
>The pipelines provided in this module are purely examples and do not necessarily represent the best IC parameters for the dataset. 

## Run the 'multi_pipelines' notebook

    # Run this script in terminal
    # move to the multiple_pipelines_example directory to access the `sh` script
    cd multiple_pipelines_example
    # run the notebook as a python script
    source run_ipynb_as_python_script.sh

## CellProfiler Parallel

To improve the speed for correcting the images, we have implemented 'CellProfiler Parallel', which utilizes multi-processing to run one plate per CPU core.