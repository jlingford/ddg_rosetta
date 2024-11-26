#!/bin/bash

CONFIG_PLT=RosettaDDGPrediction/config_plot

rosetta_ddg_plot \
    -i ddg_mutations_aggregate.csv \
    -o key_muts \
    -cp $CONFIG_PLT/contributions_barplot.yaml

echo "done rosetta ddg plot!"
