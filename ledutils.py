#!/usr/bin/env python
# coding: utf-8

# # LED utilities
# 
# Eduardo Schiavo v. 1.0
# 
# Utilities to analyze results of Local Energy Decomposition (LED) calculations performed with the ORCA program
# 

# In[1]:


import numpy as np 
import math
import re
import matplotlib.pyplot as plt 
import matplotlib.gridspec as gridspec
import pandas as pd

# In[3]:


class DataCollect():      #Basically a collection of Curve objects
    
    def __init__(self, total, scf, disp):
        self.total = total   #Curve object with the total interaction
        self.disp  = disp    #Curve object with the dispersion contribution
        self.scf= scf        #DataCollect.subtract_curves(self.total, self.disp)
        
class DlpnoCollect():    #Similar to DataCollect, but with different contributions. The two classes may be merged at some point...
    
    def __init__(self, tot=None, SCF=None, ccsd=None, triples=None, hf=None, int_frag_1=None, int_frag_2=None, elstat=None, exch=None, disp=None, non_disp=None, ref_elec=None ):
        self.tot=tot
        self.ccsd=ccsd
        self.triples=triples
        self.hf=hf
        self.int_frag_1=int_frag_1
        self.int_frag_2=int_frag_2
        self.elstat=elstat
        self.exch=exch
        self.disp=disp
        self.non_disp=non_disp
        self.ref_elec=ref_elec
        self.scf=None #Not actually part of the LED. Its defined as tot-disp. Used to compare with DFT without D correction
        

        
        
class Curve():      #This one is pretty self-explenatory
    
    def __init__(self):
        self.x_dat = []
        self.y_dat = []

class Struct():
    
    def __init__(self,label=None, tot=None, ccsd=None, triples=None, hf=None, int_frag_1=None, int_frag_2=None, elstat=None, exch=None, disp=None, non_disp=None ):
        self.label=label
        self.tot=tot
        self.ccsd=ccsd
        self.triples=triples
        self.hf=hf
        self.int_frag_1=int_frag_1
        self.int_frag_2=int_frag_2
        self.elstat=elstat
        self.exch=exch
        self.disp=disp
        self.non_disp=non_disp


# In[4]:


###DEFINE HERE THE NEW CLASSES FOR THE DLPNO SCAN ANALYSIS

class Parser():
    

    
    def curve_from_dat(ifile, ener_a, ener_b):      #convert a .dat file in a curve object
        #ifile: str; input file  es. 'trjact.dat'
        #ener_a, ener_b: float, energy of the monomers 
    
        mydata = Curve()
        with open(ifile) as trjact:
            data = [line.strip() for line in trjact if line.strip()]

            for i in data:
                mydata.x_dat.append(float(i.split()[0]))
                mydata.y_dat.append((float(i.split()[1])-ener_a-ener_b)*2625.5)
        return mydata
    
    def collect_data(afile, bfile, e_aa, e_ab, e_ba, e_bb): #Read two .dat file with total and scf energy and return a DataCollect object
        #afile, bfile: str: input files (i.e. trjact.dat and trjscf.dat files)
        #e_aa, e_ab, e_ba, e_bb: float, act and disp energy of the monomers

        act=Parser.curve_from_dat(afile, e_aa, e_ab) #parse file with actual energy
        e_a_scf=e_aa-e_ba  #remove dispersion from optimized monomers to get scf value
        e_b_scf=e_ab-e_bb


        scf=Parser.curve_from_dat(bfile, e_a_scf, e_b_scf) #parse file with scf energy


        disp = Curve()
        disp.x_dat= act.x_dat
        for i in range(len(act.y_dat)):
            disp.y_dat.append(act.y_dat[i] - scf.y_dat[i]) #subtract act and scf to get dispersion energy
            
        MyCollect=DataCollect(act, scf, disp) #instanciate DataCollect object
        
        return MyCollect


    def struct_from_led(ifile):      #Create a Struct object from the led.dat file of the monomers
        with open(ifile) as ifile:
            data=[line.strip() for line in ifile ]
            
            MyStruct=Struct()
    
            for i in range(len(data)):
                
                if 'E(0)' in data[i] and 'REFERENCE' not in data[i]:                    
                    MyStruct.hf=float(data[i].split()[2])
                if 'E(CORR)' in data[i]:
                    MyStruct.ccsd=float(data[i].split()[2])
                if 'Triples' in data[i]:
                    MyStruct.triples=float(data[i].split()[4])
                if 'E(CCSD(T))' in data[i]:
                    MyStruct.tot=float(data[i].split()[2])
                #Next entries are only for dimers (i.e. actual LED calculations)
                if 'Intra fragment   1 (REF.)' in data[i]:
                    MyStruct.int_frag_1=float(data[i].split()[4])
                if 'Intra fragment   2 (REF.)' in data[i]:
                    MyStruct.int_frag_2=float(data[i].split()[4])
                if 'Electrostatics' in data[i]:
                    MyStruct.elstat=float(data[i].split()[2])
                if 'Exchange' in data[i]:
                    MyStruct.exch=float(data[i].split()[2])
                if 'Dispersion (strong pairs)' in data[i] and 'Dispersion (weak pairs)' in data[i+1]:
                    dispSP=float(data[i].split()[3])
                    dispWP=float(data[i+1].split()[3])
                    MyStruct.disp=dispSP+dispWP
                if 'Non dispersion (strong pairs)' in data[i] and 'Non dispersion (weak pairs)' in data[i+1]:
                    nonDispSP=float(data[i].split()[4])
                    nonDispWP=float(data[i+1].split()[4])
                    MyStruct.non_disp=nonDispSP+nonDispWP
                    
            return MyStruct 
    
    def struct_list_from_led_scan(ifile): #Create a list of Struct objects for each point of the scan from the led of the scan
        with open(ifile) as ifile:
            data=[line.strip() for line in ifile ]
            data=list(dict.fromkeys(data))

            str_list=[]                    #Create list
            for i in range(13):
                str_list.append(Struct())  #Pouplate list with Struct objects
                str_list[i].name=i+1

            ##### GET STRUCT OBJECTS' ATTRIBUTES
            for i in range(len(data)):

                if ':E(0)' in data[i]:
                    lines=re.split('_|\.|\... ', data[i], maxsplit=8)
                    str_list[int(lines[3])-1].hf=float(lines[8])
  

                if 'E(CORR)' in data[i]:
                    lines=re.split('_|\.|\... ', data[i], maxsplit=8)
                    str_list[int(lines[3])-1].ccsd=float(lines[8])

                if 'Triples' in data[i]:
                    lines=re.split('_|\.|\... ', data[i], maxsplit=8)
                    str_list[int(lines[3])-1].triples=float(lines[8])
                if 'E(CCSD(T))' in data[i]:
                    lines=re.split('_|\.|\... ', data[i], maxsplit=8)
                    str_list[int(lines[3])-1].tot=float(lines[8])

                if 'Intra fragment   1' in data[i]:
                    lines=re.split('_|\.|\) ', data[i], maxsplit=7)
                    str_list[int(lines[3])-1].int_frag_1=float(lines[7])

                if 'Intra fragment   2' in data[i]:
                    lines=re.split('_|\.|\) ', data[i], maxsplit=7)
                    str_list[int(lines[3])-1].int_frag_2=float(lines[7])

                if 'Electrostatics' in data[i]:
                    lines=re.split('_|\.|\) ', data[i], maxsplit=7)
                    str_list[int(lines[3])-1].elstat=float(lines[7])

                if 'Exchange' in data[i]:
                    lines=re.split('_|\.|\) ', data[i], maxsplit=7)
                    str_list[int(lines[3])-1].exch=float(lines[7])

                if 'Dispersion (strong pairs)' in data[i] and 'Dispersion (weak pairs)' in data[i+1]:
                    lines=re.split('_|\.|\) ', data[i], maxsplit=6)
                    flines=re.split('_|\.|\) ', data[i+1], maxsplit=6)

                    str_list[int(lines[3])-1].disp=float(lines[6])+float(flines[6])

                if 'Non dispersion (strong pairs)' in data[i] and 'Non dispersion (weak pairs)' in data[i+1]:
                    lines=re.split('_|\.|\) ', data[i], maxsplit=6)
                    flines=re.split('_|\.|\) ', data[i+1], maxsplit=6)

                    str_list[int(lines[3])-1].non_disp=float(lines[6])+float(flines[6])
            return str_list
        
    def dlpno_collect_from_led_scan(afile, bfile, cfile):

        str_list=Parser.struct_list_from_led_scan(afile)
        mono1=Parser.struct_from_led(bfile)
        mono2=Parser.struct_from_led(cfile)

        MyDlpnoCollect=DlpnoCollect()  

        MyDlpnoCollect.tot=Curve()
        MyDlpnoCollect.hf=Curve()
        MyDlpnoCollect.disp=Curve()
        MyDlpnoCollect.ccsd=Curve()
        MyDlpnoCollect.triples=Curve()
        MyDlpnoCollect.int_frag_1=Curve()
        MyDlpnoCollect.int_frag_2=Curve()
        MyDlpnoCollect.elstat=Curve()
        MyDlpnoCollect.exch=Curve()
        MyDlpnoCollect.non_disp=Curve()
        MyDlpnoCollect.ref_elec=Curve()
        MyDlpnoCollect.scf=Curve()

        x_dat=np.arange(2.5, 5.75, 0.25)

        MyDlpnoCollect.tot.x_dat=x_dat
        MyDlpnoCollect.hf.x_dat=x_dat
        MyDlpnoCollect.disp.x_dat=x_dat
        MyDlpnoCollect.ccsd.x_dat=x_dat
        MyDlpnoCollect.triples.x_dat=x_dat
        MyDlpnoCollect.int_frag_1.x_dat=x_dat
        MyDlpnoCollect.int_frag_2.x_dat=x_dat
        MyDlpnoCollect.elstat.x_dat=x_dat
        MyDlpnoCollect.exch.x_dat=x_dat
        MyDlpnoCollect.non_disp.x_dat=x_dat
        MyDlpnoCollect.ref_elec.x_dat=x_dat
        MyDlpnoCollect.scf.x_dat=x_dat

        for i in range(13):
            #LED TERMS: all the terms from .hf on should add app to .tot
            MyDlpnoCollect.tot.y_dat.append((str_list[i].tot-mono1.tot-mono2.tot)*2625.5) #get curves and convert to kJ/mol
            MyDlpnoCollect.hf.y_dat.append((str_list[i].hf-mono1.hf-mono2.hf)*2625.5)
            MyDlpnoCollect.triples.y_dat.append((str_list[i].triples-mono1.triples-mono2.triples)*2625.5)
            MyDlpnoCollect.disp.y_dat.append(str_list[i].disp*2625.5) 
            MyDlpnoCollect.elstat.y_dat.append((str_list[i].elstat)*2625.5)
            MyDlpnoCollect.exch.y_dat.append((str_list[i].exch)*2625.5)            
            
            MyDlpnoCollect.non_disp.y_dat.append((str_list[i].non_disp-mono1.ccsd-mono2.ccsd)*2625.5)
            
            MyDlpnoCollect.ref_elec.y_dat.append(((str_list[i].int_frag_1-mono1.hf)+(str_list[i].int_frag_2-mono2.hf))*2625.5)
            
            
            
            #NOT really part of the LED
            MyDlpnoCollect.ccsd.y_dat.append(str_list[i].ccsd)           
            
            MyDlpnoCollect.int_frag_1.y_dat.append(str_list[i].int_frag_1)
            MyDlpnoCollect.int_frag_2.y_dat.append(str_list[i].int_frag_2)
            #Not defined in LED. scf=tot-disp. Used to compare with SCF from DFT withoud D correction
            MyDlpnoCollect.scf.y_dat.append(((str_list[i].tot-mono1.tot-mono2.tot)-str_list[i].disp)*2625.5)

            

        return MyDlpnoCollect
    
    def get_charges(ifile, n_at1, n_at2):
        #ifile, str: nbo_charges file 
        #n_at1, n_at2, int: number of atoms in fragments 1 and 2. Including ghost atoms!!
        with open(ifile) as ifile:
            data=[]
            for line in ifile:
                data.append(line.split())

            MyCurve=Curve()
            x_dat=np.arange(2.5, 5.75, 0.25)
            MyCurve.x_dat=x_dat


            mydata=np.empty([13,2])


            jump=0
            for k in range(0, 13):

                f1_len= n_at1 #Number of atoms in fragment 1. Including ghost atoms!  
                f2_len= n_at2 #Number of atoms in fragment 2. Including ghost atoms!

                mydata[k][0]=re.split('_|\.', data[jump][0])[3]

                frag_1=[]
                frag_2=[]
                for i in range(3+jump, 3+jump+f1_len):
                    frag_1.append(float(data[i][3]))
                mydata[k][1]=sum(frag_1)
        #         print(sum(frag_1))

                for j in range(3+jump+f1_len, 3+f1_len+jump+f2_len):
                    frag_2.append(float(data[j][3]))
        #         print(sum(frag_2))

                jump+=f1_len+f2_len+5

                if math.isclose(sum(frag_1), -sum(frag_2), abs_tol=1e-04):
                     pass
                else:
                    print('Error! The charge lost by one fragment does not match that gained by the other one!')

        ind=np.argsort(mydata[:,0])
        out=mydata[ind]
        MyCurve.y_dat=out[:,1]
        # ind=np.argsort(a[:,-1])
        return MyCurve


    

#
#STANDALONE FUNCTIONS
#
#Computes the LED Deltas from Struct Objects and returns the components as a dict
def compute_led_components(dimer, frag1, frag2, name=None, as_column=False):
    #dimer, frag1, frag2: Struct Objects containing the LED data for the dimer and the two fragments
    #
    #as_column: bool (optional), print dataframe as column or row. default==False
    #
    #name: string, Name to be assigned as index in the Dataframe
    
    deltaTot=dimer.tot-frag1.tot-frag2.tot
    deltaTriples=dimer.triples-frag1.triples-frag2.triples
    elPrepFrag1=dimer.int_frag_1-frag1.hf
    elPrepFrag2=dimer.int_frag_2-frag2.hf
    elPrepTot=elPrepFrag1+elPrepFrag2
    elstat=dimer.elstat
    exch=dimer.exch
    disp=dimer.disp
    nonDisp=dimer.non_disp-frag1.ccsd-frag2.ccsd
    #Create Dictionary
    ledDict={r'$\Delta$E(CCSD(T))':deltaTot,\
            r'$\Delta$E(T)':deltaTriples,\
            r'$\Delta$E(el-prep)':elPrepTot,\
            'Eelstat':elstat,\
            'Eexch':exch,\
            'Edisp':disp,\
            r'$\Delta$E(non-disp)':nonDisp}
   
    #Create DataFrame
    if as_column==True:
        ledDataFrame=pd.DataFrame.from_dict(ledDict, orient='index')
        #Check if LED adds up
        isok=math.isclose(ledDataFrame.iloc[1:,0].sum(), ledDataFrame.iloc[0,0], abs_tol=1e-04)
    else:
        ledDataFrame=pd.DataFrame(ledDict, index=[name])
        #Check if LED adds up
        isok=math.isclose(ledDataFrame.iloc[0,1:].sum(), ledDataFrame.iloc[0,0], abs_tol=1e-04)

 
    #Print Warning if LED does not add up
    if isok==False:
        print('WARNING: the sum of the LED components does not match the total DeltaE')
    else:
        pass
    
    return ledDataFrame
    
