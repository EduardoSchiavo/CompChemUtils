#!/usr/bin/env python
# coding: utf-8

# ## Crest Utilities
# 
# Module containing functions and utilities for crest analysis

# In[8]:


import matplotlib.pyplot as plt
import pandas as pd


# ## crest to dataframe
# 
# takes the crest.out input and returns a pandas DataFrane object

# In[35]:


def crest_to_dataframe(crest_out):


    with open(crest_out, 'r') as ifile:
        #initialize DataFrame
        conformers=pd.DataFrame(columns=['Number','Weight','Energy (Eh)'])

        for line in ifile:
            if "total number unique points" in line:
                unique_points=int(line.split()[7]) # get total number of structures 
                rows=ifile.readlines()[1:unique_points]    #rows f the table

                for i,row in  enumerate(rows):  
                    if len(row.split())>6:     #isolate rows containing 'real conformers'
                        #read number, energy and weight
                        conf_num=int(row.split()[5])
                        conf_energy=float(row.split()[2])
                        conf_weight=float(row.split()[3])                        
                        #assign to DataFrame
                        conformers=conformers.append({'Number':conf_num, 'Weight':conf_weight, 'Energy (Eh)':conf_energy}, ignore_index=True)
                        

    return conformers

#Add one column with energies shifted w.r.t the lowest one and converted to kJ/mol
def add_shifted_energies(dataframe):
    shifted_E=(dataframe['Energy (Eh)']-dataframe['Energy (Eh)'][0])*2625.5
    dataframe[r'$\Delta$E (kJ mol$^{-1}$)']=shifted_E
    return dataframe


# In[36]:


df=crest_to_dataframe('crest.out')
# df.set_index('Number')
df=add_shifted_energies(df)
df.head()


# In[ ]:




