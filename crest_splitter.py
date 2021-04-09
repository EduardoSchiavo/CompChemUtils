#!/usr/bin/env python
# coding: utf-8

# # ORCA utilities
# 
# Utilities for input creation and output post-processing

# ## Geometry Splitter for CREST conformers



with open('crest_conformers.xyz') as ifile:

        name=input('Enter name of the fragments: ')
        func=input('Which functional? ')
        disp=input('Which dispersion correction? ')
        atn = int(input('How many atoms? '))
        geo_num=int(input('How many conformations? '))
        basis =input('Which basis set? ')


        N=0

        for line in ifile:
#             print(line)
            if str(atn) in line.split(): #Use occurrences of the atom number line to count the geometries
                N=N+1

                with open("{0}_{1}_{2}.inp".format(name, func, N), 'w') as output:
                    output.write('!' + func + " " + disp + " "+ basis + "\n")
                    output.write("\n")
                    output.write("%pal nprocs 8 end\n")
                    output.write("\n")
                    output.write('*xyz 0 1\n')
                    a=next(ifile)
                    for i in range(atn):
                        output.write(next(ifile))
                    output.write('*')


        
        
 
