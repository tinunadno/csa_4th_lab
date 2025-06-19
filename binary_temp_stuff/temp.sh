for ((i = 0; i < 5000; i++))
do
	echo $(($i*$i*$i)) >> bin$i
done

