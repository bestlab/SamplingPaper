#!/bin/bash
#$ -S /bin/bash
#$ -N md
#$ -r n -j y -cwd  -q all.q
#$ -pe openmpi_singlenode 4
#$ -l mem_free=1G
source /sbcb/packages/modules/init
module add gromacs openmpi
mpirun gmx mdrun_mpi -v -stepout 1000 -deffnm md
