#!/usr/bin/env bash

cp /media/jandom/STORAGE_3/Projects/PhD/SBCB/Membrane_Protein_Folding/implicit_solvent/martini_2.1/popc/bilayer/run_1/restraints/confout.gro popc_bilayer.gro
python Protein/select.py popc_bilayer.gro popc_bilayer_new.gro -s "not name C5B"

editconf -f Protein/conf.pdb -o protein.gro -box 6.90120   6.16651   8.35485
python merge.py -i protein.gro popc_bilayer_new.gro -o conf.gro
editconf -f conf.gro -o conf.gro -box 6.90120   6.16651   8.35485

cp Protein/Protein_?.itp .

python topol.py -i conf.gro > topol.top

#grompp
#mdrun
#cp confout.gro conf.gro

~/Programs/gromacs/4.5.5/bin/grompp -f membed.mdp -maxwarn 2
~/Programs/gromacs/4.5.5/bin/g_membed -f topol.tpr -maxwarn 1 -v << EOF
Protein
non-Protein
EOF

cp membedded.gro conf.gro
python topol.py -i conf.gro > topol.top
