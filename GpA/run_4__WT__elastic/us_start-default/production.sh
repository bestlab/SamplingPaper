
#cp ../restraints/workdir/confout.gro conf.gro
#cp ../us_start-together/frame.gro conf.gro 
cp ../us_start-together/conf . -r 
cp ../assembly/*.top .
cp ../assembly/*.itp .


rm tpr/*
for i in {0..15}; do 
    grompp -c conf/conf${i}.gro -o tpr/topol${i}.tpr -maxwarn 1
done
rm \#* 

qsubmit.py --topol topol.tpr --jobname "GpA_cg-default" --cluster biowulf2 --partition niddk --nodes 4 --script=submit.sh --duration 24:00:00


#qsubmit.py --topol topol.tpr --jobname "GpA-together-cg" --cluster biowulf2 --partition niddk --nodes 4 --script=submit.sh --duration 24:00:00


