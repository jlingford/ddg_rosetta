#!/usr/bin/bash

# The rosetta_ddg_aggretate module has too much info for the plotting step
# This script takes only the ΔΔG values ("ddg" entries under the "state" column) and aggregates them again
# Input: the ddg_mutations_structures.csv
# Output: a .csv with just two columns --> the mutations names and their ΔΔG values.
# Usage: `./scripts/summarise_agg_ddg_data.sh <path/to/dir>`

# take first argument
PATH_TO_DIR=$1

# make tmp dir
mkdir -p ${PATH_TO_DIR}/tmp

# get only the three relevant columns
awk -F, '{OFS=","; print $2, $5, $8}' ${PATH_TO_DIR}/ddg_mutations_structures.csv >${PATH_TO_DIR}/tmp/tmp1.csv

# extract only the rows with ddg values
grep "ddg" ${PATH_TO_DIR}/tmp/tmp1.csv >${PATH_TO_DIR}/tmp/tmp2.csv

# add the header back
sed -i "1 e head -n 1 ${PATH_TO_DIR}/tmp/tmp1.csv" ${PATH_TO_DIR}/tmp/tmp2.csv

# get only the two relevant columns now
cut -d, -f1,3 ${PATH_TO_DIR}/tmp/tmp2.csv >${PATH_TO_DIR}/rosetta_ddg_scores.csv
