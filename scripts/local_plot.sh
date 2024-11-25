#!/bin/bash

CONFIG_PLT=RosettaDDGPrediction/config_plot

rosetta_ddg_plot \
    -i agg_data/ddg_mutations_structures.csv \
    -o key_muts \
    -cp $CONFIG_PLT/total_heatmap.yaml

echo "done rosetta ddg plot!"
