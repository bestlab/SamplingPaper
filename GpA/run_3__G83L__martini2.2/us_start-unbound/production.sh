
#cp ../restraints/confout.gro conf.gro
cp ../us_start-together/conf/conf15.gro conf.gro 
cp ../assembly/*.top .
cp ../assembly/*.itp .

rm tpr/*
for i in {0..15}; do 
    grompp -c conf.gro -o tpr/topol${i}.tpr -maxwarn 1
done
rm \#* 

qsubmit.py --topol topol.tpr --jobname "GpA_cg-separate" --cluster biowulf2 --partition niddk --nodes 4 --script=submit.sh --duration 24:00:00

#qsubmit.py --topol topol.tpr --jobname "GpA-together-cg" --cluster biowulf2 --partition quick --nodes 2 --script=submit.sh --duration 01:00:00
#echo System | trjconv -pbc mol -f workdir__separate/traj15.xtc -dump 50e3 -s tpr/topol0.tpr -o frame.gro 

#for i in {0..15}; do
#	echo System | trjconv -pbc mol -f workdir/traj${i}.xtc -dump 100e3 -s tpr/topol0.tpr -o conf/conf${i}.gro 
#done
