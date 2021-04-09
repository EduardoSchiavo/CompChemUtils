#!/bin/bash

#This setting was used for the scans input. It can be removed if there are no dummy atoms
for i in *.inp; do
	sed -i 's/- /DA/g' $i       #substitute dummy atoms name "-" to "DA"
done

#Submit all *inp files with the suborca script
for i in * inp; do
/csnfs/software/orca/suborca -c -q xe30th ${i%.inp}  #submit all inputs
done
