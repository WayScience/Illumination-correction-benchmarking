#!/bin/bash

# Modified Jenna's nf1_ic.ipynb file from the Cellpainting repo
# https://github.com/WayScience/nf1_cellpainting_data/blob/main/2.cellprofiler_analysis/nf1_analysis.sh

# initialize the correct shell for your machine to allow conda to work (see README for note on shell names)
conda init bash
# activate the main conda environment
conda activate IC_bench_4.2.6

# convert all notebooks to python files into the scripts folder
jupyter nbconvert --to python --output-dir=scripts/ *.ipynb

# run the python scripts in order (CellProfiler analysis then rename SQLite files)
python scripts/nf1_analysis.py
python scripts/rename_sqlite_files.py
