

rm tpr/*

for i in {0..31}; do 
	grompp -c conf/conf31.gro -o tpr/topol${i}.tpr -maxwarn 2 -n
	#break
done

rm mdout.mdp \#*
