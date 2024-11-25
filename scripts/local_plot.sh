#!/bin/bash

CONFIG_PLT=RosettaDDGPrediction/config_plot

rosetta_ddg_plot \
    -i data_keymuts1/agg_data/G34R_aggregate.csv \
    -o key_muts \
    -cp $CONFIG_PLT/contributions_barplot.yaml

echo "done rosetta ddg plot!"
