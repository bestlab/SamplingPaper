
cp ../restraints/confout.gro conf.gro
cp ../assembly/*.top .
cp ../assembly/*.itp .

rm tpr/*
for i in {0..2}; do
    grompp -c conf.gro -o tpr/topol${i}.tpr -maxwarn 1
done
rm \#*

qsubmit.py --topol topol.tpr --jobname "GpA_cg-debug" --cluster biowulf2 --partition niddk --nodes 1 --script=submit.sh --duration 24:00:00
