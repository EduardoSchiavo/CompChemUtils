#!/usr/bin/env python3

#############################################
#           LED COLLECTOR FOR HFLD          #
#############################################
#
#Generates a .csv from the ORCA output with LED 
# from the HFLD
# 
# CALL AS:
# 
# ./get_hfld.py <orca_out_filename.out> <output_csv_fileneame.csv>
import regex as re
import sys

def write_to_csv(output_filename: str, indexes: list, led_matches, intra_matches)-> None:
    """
    takes list of dimer indices and matches and prints to csv
    """
    with open(output_filename, 'w') as ofile:
        #print block of Intra fragment reference energies
        for match in intra_matches:
            ofile.write(match.group(1) + "," +\
                match.group(2) + "," +\
                match.group(3) + "," +\
                match.group(4) + "\n")
        #blank lines
        ofile.write("\n\n")
        #write LED block
        count=0
        for match in led_matches:
            if count == 0 or count % 5 == 0:
                try:
                    ofile.write(str(indexes[int(count / 5)][0]) +\
                        "," + str(indexes[int(count / 5)][1] + "\n"))
                except IndexError:
                    print("reached end of dimer indexes list")
                    break
                count+=1
            ofile.write(match.group(1) + "," + match.group(2) + "\n")
            count+=1

def get_matches(input_string:str, regular_expression: str):
    """
    take a string and a regex and return matches as a _regex.Scanner object
    """
    pattern=re.compile(regular_expression)
    return pattern.finditer(input_string)


if __name__ == '__main__':
    # get I/O filenames
    IFILE=sys.argv[1]
    OFILE=sys.argv[2]

    #concert input file to string
    with open(IFILE) as hfld_file:
        hfld_string=hfld_file.read()

    # #match reference energies
    intra_matches=get_matches(hfld_string, r'(Intra\sfragment)\s+(\d{1,2})\s(\(REF\.\))\s+([-]?\d+\.\d{9})')
    #match LED decomposition of fragments
    led_matches=get_matches(hfld_string, r'(\w+\s\(.*\.?\)\s+)([-]?\d\.\d{9})')
    #match dimer indexes e.g. Interaction of fragments 17 and 12:
    dim_matches=get_matches(hfld_string, r'Interaction of fragments\s{1,2}(\d{1,2})\sand\s{1,2}(\d{1,2})' )
    #convert to list of tuples of indices
    dim_indexes=[]
    for dim in dim_matches:
        dim_indexes.append((dim.group(1), dim.group(2)))

    write_to_csv(OFILE, dim_indexes, led_matches, intra_matches)
