#!/usr/bin/env bash


#source ~/Programs/gromacs/4.5.5/bin/GMXRC

cp ../minimization/confout.gro conf.gro
cp ../assembly/*.top .
cp ../assembly/*.itp .

grompp -maxwarn 1

mdrun -v -rdd 1.7

trjconv -dump 50e3 -pbc mol -o frame-50ns.gro
