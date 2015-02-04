#!/bin/bash

# use the following to install software needed to run the demo code in BCE

# if using BCE via VirtualBox, before starting the BCE VM, go to Machine > Settings, select System and increase the number of processors

sudo apt-get install libopenblas-base libopenblas-dev

Rscript -e "install.packages(c('RhpcBLASctl', 'Rmpi', 'doMPI'), repos = 'http://cran.cnr.berkeley.edu')"

sudo apt-get install libopenmpi-dev openmpi-bin

sudo pip install mpi4py

