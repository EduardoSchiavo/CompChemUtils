#!/usr/bin/python3


#First version of Geom Splitter
# 
#Taking as an input the geometries from a rigid scan done with %params
#
#Outputs an ORCA input for each geometry in the geoms.txt file


with open('geoms.txt') as ifile:
        
        name=input('Enter name of the fragments: ')
        func=input('Which functional? ')
        disp=input('Which dispersion correction?')
        atn = int(input('How many atoms? '))
        basis = "def2-QZVPP"
        
        for line in ifile:
            #print(line)
            for part in line.split():
                if "Geometry" in part:
                    
                    with open("{0}_{1}_{2}.inp".format(name, func, line.split()[2]), 'w') as output:
                        output.write('!' + func + " " + disp + " "+ basis + "\n")
                        output.write("\n")
                        output.write("%pal nprocs 8 end\n")
                        output.write("\n")
                        output.write('*xyz 0 1')
                        for i in range(atn+1):
                            output.write(next(ifile)[16:])
                        output.write('*')

