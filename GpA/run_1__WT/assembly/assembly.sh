#!/usr/bin/env bash

editconf -f Protein/chain.pdb -box 6.31915   6.46099  10.05482 -o protein.gro
genbox -cp protein.gro -cs dppc_bilayer.gro

genconf -f out.gro -o out.gro -nbox 2 1 1

python Protein/select.py out.gro protein.gro -s "protein "
python Protein/select.py out.gro lipids.gro -s "resname DPPC"
python Protein/select.py out.gro water.gro -s "resname W"

touch vdwradii.dat
python merge.py -i protein.gro lipids.gro water.gro -o conf.gro
editconf -f conf.gro -o conf.gro -box 12.63830   6.46099  10.05482

cp Protein/Protein_A.itp .
python topol.py -i conf.gro > topol.top

exit 0

#genconf -f dppc_bilayer.gro -nbox 2 1 1 -o bilayer.gro
python Protein/select.py dppc_bilayer.gro lipids.gro -s "resname DPPC"
python Protein/select.py dppc_bilayer.gro water.gro -s "resname W"
genconf -f lipids.gro -nbox 2 1 1 -o lipids.gro
genconf -f water.gro -nbox 2 1 1 -o water.gro

editconf -f Protein/chain.pdb -box 6.31915   6.46099  10.05482 -o protein.gro
genconf -f protein.gro -nbox 2 1 1 -o protein.gro

cp Protein/Protein_A.itp .

touch vdwradii.dat
python merge.py -i protein.gro bilayer.gro -o conf.gro
editconf -f conf.gro -o conf.gro -box 12.63830   6.46099  10.05482

python topol.py -i conf.gro > topol.top
~/Programs/gromacs/4.5.5/bin/grompp -f membed.mdp -maxwarn 1
~/Programs/gromacs/4.5.5/bin/g_membed -f topol.tpr -maxwarn 1 -v << EOF
Protein
non-Protein
EOF

cp membedded.gro conf.gro
python topol.py -i conf.gro > topol.top

exit 0
cp /media/jandom/STORAGE_3/Projects/PhD/SBCB/Membrane_Protein_Folding/implicit_solvent/martini_2.1/popc/bilayer/run_1/restraints/confout.gro popc_bilayer.gro
python Protein/select.py popc_bilayer.gro popc_bilayer_new.gro -s "not name C5B"

editconf -f Protein/conf.pdb -o protein.gro -box 6.90120   6.16651   8.35485
python merge.py -i protein.gro popc_bilayer_new.gro -o conf.gro
editconf -f conf.gro -o conf.gro -box 6.90120   6.16651   8.35485

cp Protein/Protein_?.itp .

python topol.py -i conf.gro > topol.top

grompp
mdrun
cp confout.gro conf.gro

~/Programs/gromacs/4.5.5/bin/grompp -f membed.mdp -maxwarn 1
~/Programs/gromacs/4.5.5/bin/g_membed -f topol.tpr -maxwarn 1 -v << EOF
Protein
non-Protein
EOF

cp membedded.gro conf.gro
python topol.py -i conf.gro > topol.top
