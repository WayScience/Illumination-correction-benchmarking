# Modifed Jenna's script (nf1_ic.sh) from the Cellpainting repo https://github.com/WayScience/nf1_cellpainting_data/blob/main/1.cellprofiler_ic/nf1_ic.sh

#!/bin/bash

# initialize the correct shell for your machine to allow conda to work 
conda init bash

# activate the main conda environment
conda activate IC_bench_4.2.6

# convert the notebook into a python script and run the file
jupyter nbconvert --to python \
        --FilesWriter.build_directory=scripts/ \
        --execute notebooks/multi_pipelines.ipynb
