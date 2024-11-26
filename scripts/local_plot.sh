#!/bin/bash

CONFIG_PLT=RosettaDDGPrediction/config_plot

rosetta_ddg_plot \
    -i ddg_mutations_structures.csv \
    -o key_muts3 \
    -cp $CONFIG_PLT/dg_swarmplot.yaml

echo "done rosetta ddg plot!"
