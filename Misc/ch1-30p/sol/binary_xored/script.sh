#!/bin/bash
counter=0
while [ $counter -lt 1000 ]
 do
 cat "$counter".dat >> output.dat
 ((counter++))
 done
echo All done
