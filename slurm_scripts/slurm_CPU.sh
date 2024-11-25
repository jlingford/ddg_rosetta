#!/bin/bash
#SBATCH --job-name="RosettaDDG"
#SBATCH --account=rp24
#SBATCH --partition=genomics
#SBATCH --qos=genomics
#SBATCH --time=4:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-core=1
#SBATCH --ntasks-per-node=48
#SBATCH --cpus-per-task=16
#SBATCH --mem=40000
#SBATCH --mail-user=james.lingford@monash.edu
#SBATCH --mail-type=BEGIN,END,FAIL,TIME_OUT
#SBATCH --chdir="/home/jamesl/rp24_scratch2/jamesl2/ddg_rosetta"
#SBATCH --output=log-%j.out
#SBATCH --error=log-%j.err

# set env
module purge
module load miniforge3
module load gcc/10.2.0
module load openmpi/4.1.2-ucx
conda activate /fs04/scratch2/rp24/jamesl2/RosettaDDGPrediction/rp24_scratch2/jamesl2/miniconda/conda/envs/ddg_rosetta

# set variables
ROSETTA_DIR=/fs04/scratch2/rp24/jamesl2/RosettaDDGPrediction/rp24_scratch2/jamesl2/miniconda/conda/envs/ddg_rosetta/bin
CONFIG_RUN=../config/config_run
CONFIG_SET=../config/config_settings
MUT_DIR=../muts

# generate help output
rosetta_ddg_run --help >help.txt

# run rosetta
rosetta_ddg_run \
    --pdbfile pdb_input/*.pdb \
    --listfile $MUT_DIR/mutlist_rosetta.txt \
    --configfile-run $CONFIG_RUN/cartesian2020_ref2015.yaml \
    --configfile-settings $CONFIG_SET/rosettanompi.yaml \
    --rosettapath $ROSETTA_DIR \
    --saturation

rosetta_ddg_check_run
