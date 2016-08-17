#!/bin/bash

module use --prepend ~/privatemodules
module add gromacs/4.6.7_plumed2.2-hrex-wenwei_icc

mpirun=`which mpirun`
application=`which mdrun`

ng=2

options="-nsteps 1000000 -multi $ng -maxh 24 -plumed -replex 1000 -s tpr/topol.tpr -x traj.xtc -pin on -rdd 1.7"

echo "Running Gromacs with $SLURM_NTASKS MPI tasks"
echo "Nodelist: $SLURM_NODELIST"

$mpirun $application $options

