
# coding: utf-8

# In[191]:


import pandas as pd
import statistics as st
import numpy as np
from __future__ import division
import plotly.plotly as py
import plotly.graph_objs as go


# In[192]:


census=pd.read_table('india-districts-census-2011.csv',sep=',') 


# In[193]:


census.head()


# In[194]:


census.rename(columns={'State name':'state_name'},inplace=True)


# In[195]:


census.rename(columns={'District name':'district_name'},inplace=True)


# In[196]:


census_bihar=census.loc[(census.state_name=="BIHAR")]


# In[197]:


census_bihar


# In[198]:


census_tamilNadu=census.loc[(census.state_name=="TAMIL NADU")]


# In[199]:


census_tamilNadu = census_tamilNadu.rename(columns={'district_name': 'tname'})



# In[200]:


census_tamilNadu


# In[201]:


census_bihar.reset_index()


# In[202]:


census_tamilNadu.reset_index()


# In[203]:



similar=[]
for index, row in census_bihar.iterrows():
    for index1,row1 in census_tamilNadu.iterrows():
        if 0.95<(census_bihar.Population[index]/census_tamilNadu.Population[index1])<1.05:
            similar.append({census_bihar.district_name[index]:census_bihar.Population[index],census_tamilNadu.tname[index1]:census_tamilNadu.Population[index1]})


# In[206]:


similar


# In[204]:


sumx=[]
sumy=[]
for i in range(0,len(similar)):
    sumx=sumx+ similar[i].keys()
    sumy=sumy+similar[i].values()


# In[205]:


data = [go.Bar(
            x=sumx,
            y=sumy
    )]

py.iplot(data, filename='basic-bar')

