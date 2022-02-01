# utilities
Scripts for input preparation and output postprocessing


## LEDUTILS
This module is used to perfomr local Energy Decomposition analyses on top of DLPNO-CCSD(T)/LED calculations performed with ORCA

Currently only works for systems without optimization i.e. no geometric preparation

1) Import ledutils as led
2) get the data using the led_extract.sh script and save the data in three separate files i.e. one for the dimer and two for the fragments
3) initialize structure objects:
`dimer=led.Parser.struct_from_led('led_outs/dimer.dat')
frag1=led.Parser.struct_from_led('led_outs/frag_1.dat')
frag2=led.Parser.struct_from_led('led_outs/frag_2.dat')`
4) compute led and get pandas dataframe:
` led_df=led.compute_led_components(dimer, frag1, frag2, name='sys_name')`

## CRESTUTILS

To be added

## HFLD UTILITIES

fragmentator.py - separates cluster in fragments (molecules) from pdb file

hfld_heatmap.py - creates a heatmap from an HFLD output

## MISC

geom_splitter.py - Taking as an input the geometries from a rigid scan done with %params
                    Outputs an ORCA input for each geometry in the geoms.txt file

cif_splitter.py - Splits a cif file containing multiple structures into separate cif files for each structure
