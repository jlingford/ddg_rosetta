# RosettaDDGPrediction

## Overview

RosettaDDGPrediction is a Python package to run Rosetta-based protocols for the prediction of the ΔΔG of stability upon mutation of a monomeric protein or the ΔΔG of binding upon mutation of a protein complex and analyze the results.

Forked from <https://github.com/ELELAB/RosettaDDGPrediction>

## Installation

```bash
# clone repo
git clone https://github.com/jlingford/ddg_rosetta.git
cd ddg_rosetta

# make python modules executable
python3 setup.py install

# install all dependencies with conda or mamba (mamba is faster)
# NOTE: rosetta dependency takes a long time to install
mamba create -n ddg_rosetta -f requirements.yaml
mamba activate ddg_rosetta
```

Upon successful installation, you should have three executable (`rosetta_ddg_run`, `rosetta_ddg_aggregate` and `rosetta_ddg_plot`) available to perform the various steps of data collection and analysis.

## Usage

Please refer to the user guide .pdf for how to use RosettaDDGPrediction.

Examples of how to run each step:

1. Run Rosetta

```bash
# ensure that pdb file is in pdb_input dir
# ensure mutations are specified in muts.txt
# the rosetta is installed under the conda or mamba dir for ddg_rosetta

rosetta_ddg_run \
    -p pdb_input/wt_monomer.pdb \
    -l muts/muts.txt \
    -cr ./config/config_run/cartddg2020_ref2015.yaml \
    -cs ./config/config_settings/rosettampi.yaml \
    -r /home/$USER/micromamba/envs/ddg_rosetta
```

This outputs two new dirs, `relax` and `cartesian`, which is populated with info required by `rosetta_ddg_aggregate`.

2. Aggregate the rosetta data

```bash
rosetta_ddg_aggregate \
    -ca ./config/config_aggregate/aggregate.yaml \
    -cr ./config/config_run/cartddg_ref2015.yaml \
    -cs ./config/config_settings/nompi.yaml \
    -mf cartesian/mutinfo.txt
```

The aggreagation step creates two .csv files required for the final plotting step

3. Plot the data

```bash
rosetta_ddg_plot \
    -i ddg_mutations_structures.csv \
    -o test3 \
    -cp ./config/config_plot/total_heatmap.yaml
```

## Citation

RosettaDDGPrediction for high-throughput mutational scans: from stability to binding

Valentina Sora, Adrian Otamendi Laspiur, Kristine Degn, Matteo Arnaudi, Mattia Utichi, Ludovica Beltrame, Dayana De Menezes, Matteo Orlandi, Olga Rigina, Peter Wad Sackett, Karin Wadt, Kjeld Schmiegelow, Matteo Tiberti, Elena Papaleo*
under revision for Protein Science and on biorxiv:  <https://doi.org/10.1101/2022.09.02.506350>
