#!/bin/bash
#SBATCH --job-name="RosettaDDG_flex"
#SBATCH --account=rp24
#SBATCH --partition=genomicsb
#SBATCH --qos=genomicsbq
#SBATCH --time=72:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=48
#SBATCH --mem=360000
#SBATCH --mail-user=james.lingford@monash.edu
#SBATCH --mail-type=BEGIN,END,FAIL,TIME_OUT
#SBATCH --chdir="/home/jamesl/rp24_scratch2/jamesl2/ddg_rosetta"
#SBATCH --output=log-%j.out
#SBATCH --error=log-%j.err

# set env
module purge
# module load openmpi/1.10.3-gcc4-mlx
module load miniforge3
conda activate /fs04/scratch2/rp24/jamesl2/ddg_rosetta/rp24_scratch2/jamesl2/miniconda/conda/envs/ddg_rosetta

# set variables
ROSETTA_DIR=/fs04/scratch2/rp24/jamesl2/ddg_rosetta/rp24_scratch2/jamesl2/miniconda/conda/envs/ddg_rosetta
CONFIG_RUN=RosettaDDGPrediction/config_run
CONFIG_SET=RosettaDDGPrediction/config_settings
CONFIG_AGG=RosettaDDGPrediction/config_aggregate
CONFIG_PLT=RosettaDDGPrediction/config_plot
MUT_DIR=muts

# generate help output
rosetta_ddg_run --help >help.txt

echo "running rosetta ddg!"

# run rosetta
rosetta_ddg_run \
    --pdbfile pdb_input/wt_dimer.pdb \
    --listfile $MUT_DIR/dimer_all_viet_muts.txt \
    --configfile-run $CONFIG_RUN/flexddg_ref2015.yaml \
    --configfile-settings $CONFIG_SET/rosettampi.yaml \
    --rosettapath $ROSETTA_DIR \
    -n 48

echo "done rosetta ddg run!"

rosetta_ddg_check_run \
    --configfile-run $CONFIG_RUN/flexddg_ref2015.yaml

echo "done rosetta check"

rosetta_ddg_aggregate \
    -ca $CONFIG_AGG/aggregate.yaml \
    -cr $CONFIG_RUN/flexddg_ref2015.yaml \
    -cs $CONFIG_SET/rosettampi.yaml \
    -mf flexddg/mutinfo.txt \
    -od flexddg_aggdata \
    -n 48

echo "running custom aggregation step"

../scripts/summarise_agg_ddg_data.sh

echo "done rosetta ddg aggregate!"

rosetta_ddg_plot \
    -i agg_data/ddg_mutations_structures.csv \
    -o key_muts \
    -cp $CONFIG_PLT/total_heatmap.yaml

echo "done rosetta ddg plot!"
