#!/bin/bash

module use --prepend ~/privatemodules
module add intel/2015.1.133 openmpi/1.8.4/intel-2015.1.133 
module add gromacs/4.6.7_plumed2.1-hrex-wenwei_icc plumed/2.1-hrex-wenwei-icc 

mpirun=`which mpirun`
application=`which mdrun`

ng=32

if [ -f state0.cpt ]; then 
    sed -i.bak -e s/"#RESTART"/"RESTART"/g plumed.dat.*
    options="-multi $ng -maxh 24 -plumed -replex 10000 -s tpr/topol.tpr -rdd 1.8 -cpi state.cpt"
else 
    options="-multi $ng -maxh 24 -plumed -replex 10000 -s tpr/topol.tpr -rdd 1.8"
fi

echo "Running Gromacs with $SLURM_NTASKS MPI tasks"
echo "Nodelist: $SLURM_NODELIST"

$mpirun $application $options

