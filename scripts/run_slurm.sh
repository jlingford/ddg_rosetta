#!/bin/bash
#SBATCH --job-name="RosettaDDG"
#SBATCH --account=rp24
#SBATCH --partition=genomics
#SBATCH --qos=genomics
#SBATCH --time=4:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=48
#SBATCH --mem=80000
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
MUT_DIR=muts

# generate help output
rosetta_ddg_run --help >help.txt

# run rosetta
rosetta_ddg_run \
    --pdbfile pdb_input/wt_monomer.pdb \
    --listfile $MUT_DIR/saturation_core_muts.txt \
    --configfile-run $CONFIG_RUN/cartesian2020_ref2015.yaml \
    --configfile-settings $CONFIG_SET/rosettampi.yaml \
    --rosettapath $ROSETTA_DIR \
    --saturation \
    --reslistfile $MUT_DIR/reslist.txt

rosetta_ddg_check_run \
    --configfile-run $CONFIG_RUN/cartesian2020_ref2015.yaml
