# utilities
Scripts for input preparation and output postprocessing

**DISCLAMER:** The modules and utilities presented in this repository are used to interact with the input or output of different computational chemistry programs and are **NOT** part of the official releases of **ANY** of those programs. These are just scripts I worte and use to speed-up my workflow. Feel free to use and or modify the scripts, but for anything related to the programs they refer to, check official documentation. 


## LEDUTILS
This module is used to perfomr local Energy Decomposition analyses on top of DLPNO-CCSD(T)/LED calculations performed with ORCA

Currently only works for systems without optimization i.e. no geometric preparation

1) Import ledutils as led
```
import ledutils as led
```

2) get the data using the led_extract.sh script and save the data in three separate files i.e. one for the dimer and two for the fragments
3) initialize structure objects:
```
dimer=led.Parser.struct_from_led('led_outs/dimer.dat')
frag1=led.Parser.struct_from_led('led_outs/frag_1.dat')
frag2=led.Parser.struct_from_led('led_outs/frag_2.dat')
```
4) compute led and get pandas dataframe:
```
led_df=led.compute_led_components(dimer, frag1, frag2, name='sys_name')
```

## CRESTUTILS

This module contains a few functions to help parse the output of a CREST (conformational analysis) calculations. 

Check here for crest documentation: https://xtb-docs.readthedocs.io/en/latest/crest.html

`crest_to_dataframe(crestout)` parses crest output file and returnds a pandas dataframe object

`add_shifted_energies(dataframe)` adds one column with energies shifted w.r.t the lowest one and converted to kJ/mol

The standalone [crest_splitter.py`](crest_splitter.py) splits the geometries from a crest output into separate files


## HFLD UTILITIES

fragmentator.py - separates cluster in fragments (molecules) from pdb file

hfld_heatmap.py - creates a heatmap from an HFLD output

## MISC

geom_splitter.py - Taking as an input the geometries from a rigid scan done with %params
                    Outputs an ORCA input for each geometry in the geoms.txt file

cif_splitter.py - Splits a cif file containing multiple structures into separate cif files for each structure
