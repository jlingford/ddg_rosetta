#!/bin/bash

# set variables
CONFIG_RUN=RosettaDDGPrediction/config_run
CONFIG_SET=RosettaDDGPrediction/config_settings
CONFIG_AGG=RosettaDDGPrediction/config_aggregate
CONFIG_PLT=RosettaDDGPrediction/config_plot

rosetta_ddg_aggregate \
    -ca $CONFIG_AGG/aggregate.yaml \
    -cr $CONFIG_RUN/cartddg_ref2015.yaml \
    -cs $CONFIG_SET/rosettampi.yaml \
    -mf cartesian/mutinfo.txt \
    -od agg_data

echo "done rosetta ddg aggregate!"

rosetta_ddg_plot \
    -i agg_data/ddg_mutations_structures.csv \
    -o key_muts \
    -cp $CONFIG_PLT/total_heatmap.yaml

echo "done rosetta ddg plot!"
