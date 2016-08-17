#!/bin/bash

module use --prepend ~/privatemodules
module add gromacs/4.6.7_plumed2.2-hrex-wenwei_icc

mpirun=`which mpirun`
application=`which mdrun`

if [ -f state.cpt ]; then 
    sed -i.bak -e s/"#RESTART"/"RESTART"/g plumed.dat*
    options="-maxh 24 -plumed -rdd 1.8 -cpi state.cpt"
else 
    options="-maxh 24 -plumed -rdd 1.8"
fi

echo "Running Gromacs with $SLURM_NTASKS MPI tasks"
echo "Nodelist: $SLURM_NODELIST"

$mpirun $application $options

