#!/bin/bash
#SBATCH --job-name="RosettaDDG_saturation"
#SBATCH --account=rp24
#SBATCH --partition=genomicsb
#SBATCH --qos=genomicsbq
#SBATCH --time=10:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=48
#SBATCH --mem=200000
#SBATCH --mail-user=james.lingford@monash.edu
#SBATCH --mail-type=BEGIN,END,FAIL,TIME_OUT
#SBATCH --chdir="/home/jamesl/rp24_scratch2/jamesl2/ddg_rosetta"
#SBATCH --output=log-%j.out
#SBATCH --error=log-%j.err

# set env
module purge
module load miniforge3
conda activate /fs04/scratch2/rp24/jamesl2/ddg_rosetta/rp24_scratch2/jamesl2/miniconda/conda/envs/ddg_rosetta

# set variables
ROSETTA_DIR=/fs04/scratch2/rp24/jamesl2/ddg_rosetta/rp24_scratch2/jamesl2/miniconda/conda/envs/ddg_rosetta
CONFIG_RUN=RosettaDDGPrediction/config_run
CONFIG_SET=RosettaDDGPrediction/config_settings
CONFIG_AGG=RosettaDDGPrediction/config_aggregate
MUT_DIR=muts

# generate help output
rosetta_ddg_run --help >help.txt

# run rosetta
rosetta_ddg_run \
    --pdbfile pdb_input/wt_monomer.pdb \
    --listfile $MUT_DIR/saturation_core_muts.txt \
    --reslistfile $MUT_DIR/reslist.txt \
    --saturation \
    --configfile-run $CONFIG_RUN/cartesian2020_ref2015.yaml \
    --configfile-settings $CONFIG_SET/rosettampi.yaml \
    --rosettapath $ROSETTA_DIR \
    -n 48

rosetta_ddg_check_run \
    --configfile-run $CONFIG_RUN/cartesian2020_ref2015.yaml

echo "done rosetta check"
echo "aggregating data..."

rosetta_ddg_aggregate \
    -ca $CONFIG_AGG/aggregate.yaml \
    -cr $CONFIG_RUN/cartddg_ref2015.yaml \
    -cs $CONFIG_SET/rosettampi.yaml \
    -mf cartesian/mutinfo.txt \
    -od agg_data \
    -n 48

echo "running custom aggregation step"

../scripts/summarise_agg_ddg_data.sh

echo "done rosetta ddg aggregate!"
