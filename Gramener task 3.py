
# coding: utf-8

# In[122]:


import pandas as pd
import statistics as st
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go


# In[123]:


census=pd.read_table('india-districts-census-2011.csv',sep=',') 

census.rename(columns={'State name':'state_name'},inplace=True)
census.rename(columns={'District name':'District_name'},inplace=True)


# In[124]:


census_trimmed = census[["state_name","District_name","Workers","Households","Agricultural_Workers","Households_with_Telephone_Mobile_Phone"]]


# In[125]:


census_trimmed=census_trimmed.groupby("state_name",as_index=False).sum()



# In[126]:


census_trimmed['perc_agri']=(census_trimmed['Agricultural_Workers']/census_trimmed['Workers']*100)
census_trimmed['perc_mobile']=(census_trimmed['Households_with_Telephone_Mobile_Phone']/census_trimmed['Households']*100)
census_trimmed


# In[127]:


census_trimmed=census_trimmed.sort_values(['perc_agri'],ascending=False)


# In[128]:


census_trimmed


# In[129]:


trace = go.Scatter(
    x = census_trimmed['state_name'],
    y = census_trimmed['perc_agri'],
    name= 'Agricultural workers(%)'
)

trace1 = go.Scatter(
    x = census_trimmed['state_name'],
    y = census_trimmed['perc_mobile'],
    name= 'mobile penetration(%)'
)


# In[130]:


data = [trace,trace1]

py.iplot(data, filename='basic-line')

