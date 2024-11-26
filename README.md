# RosettaDDGPrediction

## Overview

RosettaDDGPrediction is a Python package to run Rosetta-based protocols for the prediction of the ΔΔG of stability upon mutation of a monomeric protein or the ΔΔG of binding upon mutation of a protein complex and analyze the results.

Forked from <https://github.com/ELELAB/RosettaDDGPrediction>

## Installation

```bash
# clone repo
git clone https://github.com/jlingford/ddg_rosetta.git
cd ddg_rosetta

# install all dependencies with conda or mamba (mamba is faster)
# NOTE: rosetta dependency takes a long time to install
mamba env create -f requirements.yaml
mamba activate ddg_rosetta

# make python modules executable
python3 setup.py install
```

Upon successful installation, you should have three executable (`rosetta_ddg_run`, `rosetta_ddg_aggregate` and `rosetta_ddg_plot`) available to perform the various steps of data collection and analysis.

## Usage

Please refer to the user guide .pdf for how to use RosettaDDGPrediction.
Modules can also be called with a `--help` flag.

Example code and scripts need to be changed per use case and won't work as is.

Examples of how to run each step:

### 1. Run Rosetta

Tested on a HPC with SLURM. Run `sbatch ./scripts/long_run_slurm.sh`

```bash
#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=48
#SBATCH <slurm stuff goes here>

## SETUP
# ensure that pdb file is in pdb_input dir
# ensure mutations are specified in muts.txt
# the rosetta is installed under the conda or mamba dir for ddg_rosetta
# check which of the .yaml config files you want to specify for running rosetta

# set env
module purge
module load miniforge3 #assuming conda is a module on your HPC
conda activate ddg_rosetta

# set variables
ROSETTA_DIR=/path/to/your/miniconda/conda/envs/ddg_rosetta #change for your system
CONFIG_RUN=RosettaDDGPrediction/config_run
CONFIG_SET=RosettaDDGPrediction/config_settings
CONFIG_AGG=RosettaDDGPrediction/config_aggregate
CONFIG_PLT=RosettaDDGPrediction/config_plot
MUT_DIR=muts

# run rosetta
rosetta_ddg_run \
    --pdbfile pdb_input/wt_monomer.pdb \
    --listfile $MUT_DIR/key_muts.txt \
    --configfile-run $CONFIG_RUN/cartesian2020_ref2015.yaml \
    --configfile-settings $CONFIG_SET/rosettampi.yaml \
    --rosettapath $ROSETTA_DIR \
    -n 48 #starts 48 processes in parallel

echo "done rosetta ddg run!"

rosetta_ddg_check_run \
    --configfile-run $CONFIG_RUN/cartesian2020_ref2015.yaml

echo "done rosetta check"
```

This outputs two new dirs, `relax` and `cartesian`, which is populated with info required by `rosetta_ddg_aggregate`.

Check the `ROSETTA_CRASH.log` to see if there were any issues.
If the run fails, the next step won't output a full .csv of all mutations.

### 2. Aggregate the rosetta data

Easiest to include this in the same SLURM script from above.

```bash

rosetta_ddg_aggregate \
    -ca $CONFIG_AGG/aggregate.yaml \
    -cr $CONFIG_RUN/cartddg_ref2015.yaml \
    -cs $CONFIG_SET/rosettampi.yaml \
    -mf cartesian/mutinfo.txt \
    -od agg_data \
    -n 48
```

The aggregation step creates two .csv files required for the final plotting step:

1. `ddg_mutations_aggregate.csv`
2. `ddg_mutations_structures.csv`

"Structures" contains all the Rosetta runs, while "aggregate" is the average of the data in "structures".
Each is specific to what sort of plot you want to generate with `rosetta_ddg_plot`.

### 3. Plot the data

Easiest to run locally after copying all the outputs to your local machine.

```bash
rosetta_ddg_plot \
    -i ddg_mutations_structures.csv \
    -o figure \
    -cp ./RosettaDDGPrediction/config_plot/total_heatmap.yaml
```

## Citation

RosettaDDGPrediction for high-throughput mutational scans: from stability to binding

Valentina Sora, Adrian Otamendi Laspiur, Kristine Degn, Matteo Arnaudi, Mattia Utichi, Ludovica Beltrame, Dayana De Menezes, Matteo Orlandi, Olga Rigina, Peter Wad Sackett, Karin Wadt, Kjeld Schmiegelow, Matteo Tiberti, Elena Papaleo*
under revision for Protein Science and on biorxiv:  <https://doi.org/10.1101/2022.09.02.506350>
