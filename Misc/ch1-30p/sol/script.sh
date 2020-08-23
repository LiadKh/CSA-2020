#!/bin/bash
for file in *; do mv "$file" $(echo "$file" | sed -e 's/[^0-9.dat]//g'); done &


counter=0
while [ $counter -lt 1000 ]
 do
 cat "$counter".dat >> output.dat
 ((counter++))
 done
echo All done
