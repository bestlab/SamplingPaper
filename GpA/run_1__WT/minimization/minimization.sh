#!/usr/bin/env bash

cp ../assembly/*.gro .
cp ../assembly/*.top .
cp ../assembly/*.itp . 

grompp -maxwarn 1

mdrun -v 

