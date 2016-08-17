

for i in {1..32}; do 
	index=$(printf "%02d\n" $i)
	j=$(($i-1))
	cp ../umbrella_windows/window${index}/window${index}.gro conf/conf${j}.gro 
done

bash build.sh

qsubmit.py --topol topol.tpr --jobname "ANT" --cluster biowulf2 --partition niddk --nodes 4 --script=submit.sh --duration 24:00:00
