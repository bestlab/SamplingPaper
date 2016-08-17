#!/bin/bash

module use --prepend ~/privatemodules
module add gromacs/4.6.7_plumed2.2-hrex-wenwei_icc

mpirun=`which mpirun`
application=`which mdrun`

ng=16

if [ -f state0.cpt ]; then
    sed -i.bak -e s/"#RESTART"/"RESTART"/g plumed.*.dat
    options="-multi $ng -maxh 24 -plumed -replex 1000 -s tpr/topol.tpr -x traj.xtc -pin on -rdd 1.8 -cpi state.cpt"
else
    options="-multi $ng -maxh 24 -plumed -replex 1000 -s tpr/topol.tpr -x traj.xtc -pin on -rdd 1.8"
fi

echo "Running Gromacs with $SLURM_NTASKS MPI tasks"
echo "Nodelist: $SLURM_NODELIST"

$mpirun $application $options

