
# coding: utf-8

# In[176]:


import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go


# In[177]:


census=pd.read_table('india-districts-census-2011.csv',sep=',') 


# In[178]:


census.rename(columns={'State name':'state_name'},inplace=True)


# In[179]:


new_columns=['state_name','Population','Literate','Households','Female_Literate','Male_Literate','Household_size_5_persons_Households','Household_size_6_8_persons_Households','Household_size_9_persons_and_above_Households']


# In[180]:


census_trimmed=pd.DataFrame(census[new_columns])


# In[182]:


census_trimmed['Literacy_Rate']=(((census_trimmed.Literate)/(census_trimmed.Population))*100)
census_trimmed['Literate_Male']=(((census_trimmed.Male_Literate)/(census_trimmed.Literate))*100)
census_trimmed['Literate_Female']=(((census_trimmed.Female_Literate)/(census_trimmed.Literate))*100)
census_trimmed['house_hold_above_5_People']=(((census_trimmed.Household_size_5_persons_Households+census_trimmed.Household_size_6_8_persons_Households+census_trimmed.Household_size_9_persons_and_above_Households)/(census_trimmed.Households))*100)


# In[183]:


new_columns2=['state_name','Literacy_Rate','Literate_Male','Literate_Female','house_hold_above_5_People']
census_trimmed=pd.DataFrame(census_trimmed[new_columns2])
census_trimmed


# In[184]:


census_trimmed=census_trimmed.groupby('state_name',as_index=False).mean()


# In[185]:


census_trimmed=census_trimmed.sort_values(by='Literacy_Rate',ascending=0)
census_trimmed.reset_index()
census_trimmed


# In[186]:


trace = go.Scatter(
    x = census_trimmed['state_name'],
    y = census_trimmed['Literacy_Rate'],
    name= 'Literacy_Rate(%)'
)

trace1 = go.Scatter(
    x = census_trimmed['state_name'],
    y = census_trimmed['house_hold_above_5_People'],
    name= 'Households with internet(%)'
)

data = [trace,trace1]

py.iplot(data, filename='basic-line')


# In[187]:


trace = go.Scatter(
    x = census_trimmed['state_name'],
    y = census_trimmed['Literacy_Rate'],
    name= 'Literacy_Rate(%)'
)

trace1 = go.Scatter(
    x = census_trimmed['state_name'],
    y = census_trimmed['Literate_Male'],
    name= 'Male literate(%)',
        line = dict(
        width = 1,
        dash = 'dash') 
)


trace2 = go.Scatter(
    x = census_trimmed['state_name'],
    y = census_trimmed['Literate_Female'],
    name= 'Female literate(%)',
        line = dict(
        width = 1,
        dash = 'dash') 
)

data = [trace,trace1,trace2]

py.iplot(data, filename='basic-line')

