#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    rosetta_ddg_aggregate.py
#
#    Aggregate data generated by running Rosetta protocols for the
#    calculation of the ΔΔG of stability/binding upon mutation.
#
#    Copyright (C) 2020 Valentina Sora 
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



# standard libary
import argparse
import logging as log
import os
import os.path
import sys
# third-party packages
import pandas as pd
import yaml
# RosettaDDGProtocols
from . import aggregation 
from .defaults import (
    CONFIGAGGRDIR,
    CONFIGAGGRFILE,
    CONFIGRUNDIR,
    ROSETTADFCOLS)
from . import util


def main():



    ######################### ARGUMENT PARSER #########################



    parser = argparse.ArgumentParser()

    cr_help = f"Configuration file of the protocol that was " \
              f"run. If it is a name without extension, it is " \
              f"assumed to be the name of a YAML file in " \
              f"{CONFIGRUNDIR}."
    parser.add_argument("-cr", "--configfile-run", \
                        type = str, \
                        required = True, \
                        help = cr_help)

    ca_help = f"Configuration file for data aggregation. " \
              f"If it is a name without extension, it is assumed " \
              f"to be the name of a YAML file in {CONFIGAGGRDIR}. " \
              f"Default is {CONFIGAGGRFILE}."
    parser.add_argument("-ca", "--configfile-aggregate", \
                        type = str, \
                        default = CONFIGAGGRFILE, \
                        help = ca_help)

    d_help = "Directory where the protocol was run. " \
             "Default is the current working directory."
    parser.add_argument("-d", "--running-dir", \
                        type = str, \
                        default = os.getcwd(), \
                        help = d_help)

    od_help = \
        "Directory where to store the aggregated data. " \
        "Default is the current working directory."
    parser.add_argument("-od", "--output-dir", \
                        type = str, \
                        default = os.getcwd(), \
                        help = od_help)

    # parse the arguments
    args = parser.parse_args()
    
    # configuration files
    configfilerun = args.configfile_run
    configfileaggr = args.configfile_aggregate
    # directories
    rundir = args.running_dir
    outdir = args.output_dir

    # get the name of the configuration file for running
    # the protocol
    configrunname = \
        os.path.basename(configfilerun).rstrip(".yaml")
    # get the name of the configuration file for data
    # aggregation
    configaggrname = \
        os.path.basename(configfileaggr).rstrip(".yaml")

    # if the configuration file is a name without extension
    if configfilerun == configrunname:
        # assume it is a configuration file in the directory
        # storing configuration files for running protocols
        configfilerun = os.path.join(CONFIGRUNDIR, \
                                     configrunname + ".yaml")
    # otherwise assume it is a file name/file path
    else:
        configfilerun = util.get_abspath(configfilerun)

    # if the configuration file is a name without extension
    if configfileaggr == configaggrname:
        # assume it is a file in the directory where
        # configuration files for data aggregation are stored
        configfileaggr = os.path.join(CONFIGAGGRDIR, \
                                      configaggrname + ".yaml")
    # otherwise assume it is a file name/file path
    else:
        configfileaggr = util.get_abspath(configfileaggr)



    ############################# LOGGING #############################



    # logging configuration
    log.basicConfig(level = log.INFO)



    ########################## CONFIGURATION ##########################



    # try to get the configuration of the run from the
    # corresponding configuration file
    try:
        configrun = util.get_config_run(configfilerun)
    # if something went wrong, report it and exit
    except Exception as e:
        errstr = f"Could not parse the configuration file " \
                 f"{configfilerun}: {e}"
    
    # try to get the configuration for data aggregation from the
    # corresponding configuration file
    try:
        configaggr = yaml.safe_load(open(configfileaggr, "r"))
    # if something went wrong, report it and exit
    except Exception as e:
        errstr = f"Could not parse the configuration file " \
                 f"{configfileaggr}: {e}"

    # get family of the protocol
    family = configrun["family"]

    # get the configuration for the output dataframes
    dfsconfig = configaggr["outdfs"]
    
    # get the options to be used in writing the output dataframes
    dfsoptions = dfsconfig["options"]
    
    # whether to rescale the scores to kcal/mol using the
    # conversion factors
    rescale = dfsconfig["rescale"]
    
    # get the columns of the output dataframes
    dfscolumns = ROSETTADFCOLS

    # get the dataframe output filenames
    dfsoutnames = dfsconfig["outnames"]
    # get the names of the aggregated output files storing data for
    # all structures or per-structure
    mutaggr = dfsoutnames["outaggregate"]
    mutstruct = dfsoutnames["outstructures"]
    # get the suffixes to be appended to each output file (all
    # structures or per-structure) concerning a single mutation
    oasuffix = dfsoutnames["outsuffixaggregate"]
    ossuffix = dfsoutnames["outsuffixstructures"]



    ############################ AGGREGATION ##########################

  

    # create empty lists to store the dataframes for each mutation
    mutaggrdfs = []
    mutstructdfs = []

    
    # if the output directory does not exist, create it
    os.makedirs(outdir, exist_ok = True)
 

    # if the protocol is a cartddg protocol
    if family == "cartddg":
        
        # get the directory where the ΔΔG calculation step was run
        rundir = os.path.join(rundir, \
                              configrun["steps"]["cartesian"]["wd"])
        
        # get the Rosetta options
        options = configrun["steps"]["cartesian"]["options"]
        
        # get the output file name
        outname = \
            options[util.get_option_key(options = options, \
                                        option = "ddgout")]

        # get the score function name
        scfname = \
            options[util.get_option_key(options = options, \
                                        option = "scfname")]
 

    # if the protocol is a flexddg protocol
    elif family == "flexddg":

        # get the directory where the ΔΔG calculation step was run
        rundir = os.path.join(rundir, \
                              configrun["steps"]["flexddg"]["wd"])
        
        # get the Rosetta options
        options = configrun["steps"]["flexddg"]["options"]
        
        # get the RosettaScript options 
        rscriptoptions = \
            options[util.get_option_key(options = options, \
                                        option = "scriptvars")]

        # get the output file name
        outname = \
            rscriptoptions[\
                util.get_option_key(options = rscriptoptions, \
                                    option = "ddgdbfile")]

        # get the score function name
        scfname = \
            rscriptoptions[\
                util.get_option_key(options = rscriptoptions, \
                                    option = "scfname")]
        
        # get the number of backrub trials
        backrubntrials = \
            rscriptoptions[\
                util.get_option_key(options = rscriptoptions, \
                                    option = "backrubntrials")]
        
        # get the backrub trajectory stride
        backrubtrajstride = \
            rscriptoptions[\
                util.get_option_key(options = rscriptoptions, \
                                    option = "backrubtrajstride")]
    
        # get the number of structures generated
        nstruct = configrun["mutations"]["nstruct"]
        
        # format the structure names as strings
        structnums = [str(num) for num in range(1, nstruct + 1)]
        
        # compute the trajectory stride
        trajstride = int(backrubntrials) // int(backrubtrajstride)


    # get the list of contributions for the scoring function used
    listcontributions = configaggr["energy_contributions"][scfname]
    
    # get the conversion factor for the scoring function used
    convfact = configaggr["conversion_factors"][scfname]  
  
    # all non-hidden directories in the running directory
    # will be considered of interest
    mutnames = [d for d in os.listdir(rundir) \
                if not d.startswith(".")]


    # for each mutation
    for mutname in mutnames:
        
        # mutation directory path
        mutpath = os.path.join(rundir, mutname)

        # if the protocol is a cartddg protocol
        if family == "cartddg":
            
            # get the path to the output file
            ddgout = os.path.join(mutpath, outname)
            
            # try to parse the output file
            try:
                df = aggregation.parse_output_cartddg(\
                        ddgout = ddgout, \
                        listcontributions = listcontributions, \
                        scfname = scfname)
            # if something went wrong, report it and continue
            except Exception as e:
                log.warning(f"Could not parse {ddgout}: {e}")
                continue
            
            # try to get the aggregated dataframes          
            try:
                dfs = aggregation.aggregate_data_cartddg(\
                        df = df, \
                        listcontributions = listcontributions)
            # if something went wrong, report it and exit
            except Exception as e:
                log.error(f"Could not aggregate data for " \
                          f"{os.path.basename(mutpath)}: {e}")
                sys.exit(1)
        
        
        # if the protocol is a flexddg protocol
        elif family == "flexddg":
            
            # initialize an empty list to store
            # dataframes for all structures
            structdfs = []
            
            # for each structure
            for structnum in structnums:
                # structure path 
                structpath = os.path.join(mutpath, structnum)
                # path to the .db3 output file 
                db3out = os.path.join(structpath, outname)
                # try to create a dataframe from the .db3 output file
                try:
                    df = aggregation.parse_output_flexddg(\
                            db3out = db3out, \
                            trajstride = trajstride, \
                            structnum = structnum, \
                            scfname = scfname)
                # if something went wrong, report it and continue
                except Exception as e:
                    log.warning(f"Could not parse {db3out}: {e}")
                    continue
                
                # append the dataframe to the list
                structdfs.append(df)

            # try to generate the aggregated dataframes            
            try:
                dfs = aggregation.aggregate_data_flexddg(\
                        df = pd.concat(structdfs), \
                        listcontributions = listcontributions)
            # if something went wrong, report it and exit
            except Exception as e:
                log.error(f"Could not aggregate data for " \
                          f"{os.path.basename(mutpath)}: {e}")
                sys.exit(1)

        
        # separate the dataframes with the wild-type ΔG, the
        # mutant ΔG and the ΔΔG
        dgwt, dgmut, ddg = dfs


        # try to generate the aggregated and all-structures dataframes
        try:
            aggrdf, structdf = aggregation.generate_output_dataframes(\
                                dgwt = dgwt, \
                                dgmut = dgmut, \
                                ddg = ddg, \
                                mutname = mutname, \
                                rescale = rescale, \
                                listcontributions = listcontributions, \
                                convfact = convfact)
        # if something went wrong, report it and exit
        except Exception as e:
            log.error(f"Could not generate output dataframes: {e}")
            sys.exit(1)


        # save the aggregated dataframe
        aggrdf.to_csv(os.path.join(outdir, mutname + oasuffix), \
                      **dfsoptions)

        # save the all-structures dataframe
        structdf.to_csv(os.path.join(outdir, mutname + ossuffix), \
                        **dfsoptions)
        
        # add the dataframes to the lists of all-mutations dataframes
        mutaggrdfs.append(aggrdf)
        mutstructdfs.append(structdf)


    # aggregate the dataframes containing single mutations
    mutaggrdf = pd.concat(mutaggrdfs)
    mutstructdf = pd.concat(mutstructdfs)
    
    # save the dataframes with data for all the mutations
    mutaggrdf.to_csv(os.path.join(outdir, mutaggr), **dfsoptions)
    mutstructdf.to_csv(os.path.join(outdir, mutstruct), **dfsoptions)


if __name__ == "__main__":
    main()