#!/usr/bin/env bash

# set variables
CONFIG_RUN=RosettaDDGPrediction/config_run
CONFIG_SET=RosettaDDGPrediction/config_settings
CONFIG_AGG=RosettaDDGPrediction/config_aggregate

rosetta_ddg_aggregate \
    -ca $CONFIG_AGG/aggregate.yaml \
    -cr $CONFIG_RUN/flexddg_ref2015.yaml \
    -cs $CONFIG_SET/rosettampi.yaml \
    -mf flexddg/mutinfo.txt \
    -od flexddg_aggdata
