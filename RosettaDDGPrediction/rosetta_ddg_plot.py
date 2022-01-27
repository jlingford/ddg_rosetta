#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    rosetta_ddg_plot.py
#
#    Plot aggregated data generated by running Rosetta protocols for
#    the calculation of the ΔΔG of stability/binding upon mutation.
#
#    Copyright (C) 2022 Valentina Sora 
#                       <sora.valentina1@gmail.com>
#                       Matteo Tiberti 
#                       <matteo.tiberti@gmail.com> 
#                       Elena Papaleo
#                       <elenap@cancer.dk>
#
#    This program is free software: you can redistribute it and/or
#    modify it under the terms of the GNU General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public
#    License along with this program. 
#    If not, see <http://www.gnu.org/licenses/>.



# Standard library
import argparse
import logging as log
import sys
# RosettaDDGProtocols
from .defaults import (
     CONFIG_AGGR_DIR,
     CONFIG_AGGR_FILE,
     CONFIG_PLOT_DIR,
     PLOT_TYPES,
     ROSETTA_DF_COLS
)
from . import plotting
from . import util



def main():



    ######################### ARGUMENT PARSER #########################



    # Set the argument parser
    parser = argparse.ArgumentParser()

    # Add arguments
    i_help = "Input CSV file (aggregated data)."
    parser.add_argument("-i", "--infile",
                        type = str,
                        required = True,
                        help = i_help)

    o_help = "Output file containing the plot."
    parser.add_argument("-o", "--outfile",
                        type = str,
                        required = True,
                        help = o_help)

    ca_help = f"Configuration file used for data aggregation. " \
              f"If it is a name without extension, it is assumed " \
              f"to be the name of a YAML file in {CONFIG_AGGR_DIR}. " \
              f"Default is {CONFIG_AGGR_FILE}."
    parser.add_argument("-ca", "--configfile-aggregate",
                        type = str,
                        default = CONFIG_AGGR_FILE, 
                        help = ca_help)

    cp_help = \
        f"Configuration file for plotting. If it is a name " \
        f"without extension, it is assumed to be the name " \
        f"of a YAML file in {CONFIG_PLOT_DIR}."
    parser.add_argument("-cp", "--configfile-plot",
                        type = str,
                        required = True, 
                        help = cp_help)


    # Parse the arguments
    args = parser.parse_args()
    
    # Files
    in_file = util.get_abspath(args.infile)
    out_file = util.get_abspath(args.outfile)
    
    # Configuration files
    config_file_plot = args.configfile_plot
    config_file_aggr = args.configfile_aggregate



    ############################# LOGGING #############################



    # Logging configuration
    log.basicConfig(level = log.INFO)



    ########################## CONFIGURATION ##########################


    
    # Try to get the configuration for data aggregation
    try:
        
        config_aggr = util.get_config_aggregate(config_file_aggr)
    
    # If something went wrong, report it and exit
    except Exception as e:
        
        errstr = f"Could not parse {config_file_aggr}: {e}"
        log.error(errstr)
        sys.exit(errstr)
    
    # Try to get the plot+output configuration
    try:
        
        config_plot = util.get_config_plot(config_file_plot)
    
    # If something went wrong, report it and exit
    except Exception as e:
        
        errstr = f"Could not parse {config_file_plot}: {e}"
        log.error(errstr)
        sys.exit(errstr)

    # Get the plot type
    plot_type = config_plot["plot"]["type"]
    
    # Get the plot options
    config = config_plot["plot"]["options"]



    ######################### PLOT GENERATION #########################

 

    # Get the configuration to be used when outputting the plot
    out_config = config_plot.get("output", {})

        
    # If the plot is a heatmap of total scores
    if plot_type == "total_heatmap":
        
        # Load the aggregated data
        df = plotting.load_aggregated_data(in_file = in_file)
        
        # Plot the heatmap
        plotting.plot_total_heatmap(df = df,
                                    config = config,
                                    out_file = out_file,
                                    out_config = out_config)


    # If the plot is a heatmap for a saturation mutagenesis scan
    elif plot_type == "total_heatmap_saturation":
        
        # Load the aggregated data
        df = plotting.load_aggregated_data(in_file = in_file,
                                           saturation = True)
        
        # Plot the 2D heatmap
        plotting.plot_total_heatmap(df = df,
                                    config = config,
                                    out_file = out_file,
                                    out_config = out_config,
                                    saturation = True)


    # If the plot is a barplot dividing the total ΔΔG score
    # into its energy contributions
    elif plot_type == "contributions_barplot":
        
        # Load the aggregated data
        df = plotting.load_aggregated_data(in_file = in_file)
        
        # Get the scoring function name
        scf_name = df[ROSETTA_DF_COLS["scf_name"]].unique()[0]
        
        # Get the list of energy cntributions for the scoring
        # function used
        contributions = config_aggr["energy_contributions"][scf_name]
        
        # Plot the bar plot
        out_config.pop("format")
        plotting.plot_contributions_barplot(\
                                    df = df,
                                    config = config,
                                    contributions = contributions,
                                    out_file = out_file,
                                    out_config = out_config)


    # If the plot is a swarmplot showing the distributions of
    # total ΔG scores for all wild-type and mutant structures
    elif plot_type == "dg_swarmplot":
        
        # Load the aggregated data
        df = plotting.load_aggregated_data(in_file = in_file)
        
        # Plot the swarmplot 
        plotting.plot_dg_swarmplot(df = df,
                                   config = config,
                                   out_file = out_file,
                                   out_config = out_config)


    # If an invalid plot type was passed, report it and exit
    else:
        errstr = f"Unrecognized plot type {plot_type}."
        log.error(errstr)
        sys.exit(errstr)


if __name__ == "__main__":
    main()