#!/usr/bin/bash

# The rosetta_ddg_aggretate module has too much info for the plotting step
# This script takes only the ΔΔG values ("ddg" entries under the "state" column) and aggregates them again
# Input: the ddg_mutations_structures.csv
# Output: a .csv with just two columns --> the mutations names and their ΔΔG values.

# make tmp dir
mkdir -p ../agg_data/tmp

# get only the three relevant columns
awk -F, '{OFS=","; print $2, $5, $8}' ../agg_data/ddg_mutations_structures.csv >../agg_data/tmp/tmp1.csv

# extract only the rows with ddg values
grep "ddg" ../agg_data/tmp/tmp1.csv >../agg_data/tmp/tmp2.csv

# add the header back
sed -i '1 e head -n 1 ../agg_data/tmp/tmp1.csv' ../agg_data/tmp/tmp2.csv

# get only the two relevant columns now
cut -d, -f1,3 ../agg_data/tmp/tmp2.csv >../agg_data/rosetta_ddg_scores.csv
