#! /usr/bin/python3

import sys

from gzdoomrun import *

#######################################
#  MM    MM    AAA    IIIIII NN   NN  # 
#  MMM  MMM   AAAAA     II   NNNN NN  #
#  MMMMMMMM  AAA AAA    II   NN NNNN  #   
#  MM MM MM AAA   AAA IIIIII NN  NNN  #
#######################################
# Processes the arguments (if any),   #
# and either preforms the specified   #
# operation, runs a specified         #
# WAD/PK3 by filname (no suffix), or  #
# runs gzdoom as is with whatever     #
# IWADs are available.                #
#######################################

if __name__ == "__main__":
    options : CommandOptions = CommandOptions(custom.load_directory())

    try:
        sys.argv.pop(0)
        options.process_arguments(len(sys.argv), sys.argv)
    
    except GZDoomRunError as e:
        e.what()