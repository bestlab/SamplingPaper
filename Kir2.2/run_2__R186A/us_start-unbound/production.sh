
cp ../restraints/workdir/confout.gro conf.gro
cp ../assembly/*.top .
cp ../assembly/*.itp .


rm tpr/*
for i in {0..15}; do 
    grompp -c conf.gro -o tpr/topol${i}.tpr -maxwarn 1 -n ../restraints/index.ndx
done
rm \#* 

python plumed.py

qsubmit.py --topol topol.tpr --jobname "Kir_cg-separate" --cluster biowulf2 --partition niddk --nodes 4 --script=submit.sh --duration 24:00:00


