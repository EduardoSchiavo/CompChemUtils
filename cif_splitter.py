#!/usr/bin/env python
#Splits a cif file containing multiple structures into separate cif files for each structure

#call as cif_splitter.cif <cif_file>

import sys

to_split=sys.argv[1]

with open(to_split, 'r') as ifile:
    for line in ifile:
        if  '_database_code_depnum_ccdc_archive' in line:
            print(line.split()[1] +' ' + line.split()[2])

            with open("strucuture_ccdc_{0}".format(line.split()[2]), 'w') as ofile:
                ofile.write('data_ \n')
                stop=False
                while stop==False:
                    try:
                        cif_line=next(ifile)
                    except StopIteration:
                        print("Reached EOF, stopping..")
                        break 
                    if '########' not in cif_line:
                        ofile.write(cif_line)
                    else:
                        stop=True

