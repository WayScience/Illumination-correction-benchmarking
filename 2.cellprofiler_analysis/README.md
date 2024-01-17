# Illumination correction, segmentation, and feature extraction using CellProfiler
In this module, we apply the illumination correction functions generated in the `1.run_multi_IC_pipelines' module as well as segment nuclei, cytoplasms, and whole cells from images and perform feature extraction using CellProfiler.

## Run the `IC_cellprofiler_analysis` notebook

To run the CellProfiler analysis pipeline on the illumination corrected images for each plate, run the [IC_cellprofiler_analysis.ipynb](IC_cellprofiler_analysis.ipynb) notebook as a python script using the code block below:

>[!Note]
>Confirm that the shell name in the [nf1_analysis.sh](nf1_analysis.sh) file is correct for your machine (e.g. Linux = `bash`, MacOS = `zsh`)

```bash
# Run this script in terminal
# move to the 2.cellprofiler_analysis directory to access the `sh` script
cd 2.cellprofiler_analysis
# run the notebook as a python script
source IC_cellprofiler_analysis.sh
```
<sub>Modifed from Jenna Tomkinson's [nf1_cellpainting_data repository](https://github.com/WayScience/nf1_cellpainting_data/tree/main/2.cellprofiler_analysis#readme)<sub>