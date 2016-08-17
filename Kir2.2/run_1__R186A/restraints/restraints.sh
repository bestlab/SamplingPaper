
editconf -f ../assembly/sys-em.pdb -o conf.gro
cp ../assembly/topol.top .
cp ../assembly/*.itp .
#cp ../assembly/em3.gro conf.gro

#grompp
grompp -n -maxwarn 1

python plumed.py

grep "  A  " kir22_together.pdb  > kir22_together-A.pdb
grep "  B  " kir22_together.pdb  > kir22_together-B.pdb
grep "  C  " kir22_together.pdb  > kir22_together-C.pdb
grep "  D  " kir22_together.pdb  > kir22_together-D.pdb

qsubmit.py --topol topol.tpr --jobname "Kir" --cluster biowulf2 --partition niddk --nodes 1 --script=submit.sh --duration 24:00:00
