# gramenerTasks
<h1>Gramener tasks for internship</h1>

Picked use case:
**Use case 2 - 2011 India Census**
Indian government carries out census every decade. This dataset contains information from the 2011 census with district level granularity on population, gender, literacy, socioeconomic status (electricity, mobiles, Internet) among a lot of other dimensions.

**Questions to answer**
1. Create a geographic map of states with low literacy rates.
2. Find out most similar districts in Bihar and Tamil Nadu. Similarity can be based on any of the columns from the data.
3. How does the mobile penetration vary in regions (districts or states) with high or low agricultural workers?

<h2>Question 1: geographical map of states with low literacy rates</h2>
![alt text](https://github.com/Jagannath-Saragadam/gramenerTasks/blob/master/Task%201.png)

According to Census a person **aged 7 or above** who can read and write with understanding in any language is called a literate person, and **Literacy Rate** is the ratio of such people to the complete population.
From the given data, the number of people in the 0-6 age range is not provided, so there is a devaition of ~10% from the actual Census statistics. 

State Name | Literacy_Rate
---------- | -------------
Bihar	| 50.39497372
Jharkhand |	54.01473957
Arunanchal Pradesh |	54.34030678
Rajasthan |	54.52011021
Jammu & Kashmir |	55.02494077
Chhattisgarh |	56.36419098
Uttar Pradesh	| 57.08807476
Madhya Pradesh	| 57.56021724
Meghalaya	| 58.81027417
Andhra Pradesh	| 59.14190755
Assam	| 61.68613029
Odisha	| 61.94152749

From the geographical map it can be infered that most of the states with low literacy rates belong to Eastern, Northern, Central and north eastern regions.
Plotting a line chat with few other attributes from the Census leads to some insights, such as:

**Literacy rate Vs. Households with more than 5 people**
![Line plot- Literacy rate Vs. Households with more than 5 people](https://github.com/Jagannath-Saragadam/gramenerTasks/blob/master/Plot%2011.png)


As the number of households with more than 5 people increase, we can see a clear dip in the literacy rate. This insight can be linked with the assumption that, as the number of people in the household increase, they get financially burdened to educate all of them.

**Literacy rate Vs. Male & Female Literate**
![Literacy rate Vs. Male & Female Literate plot](https://github.com/Jagannath-Saragadam/gramenerTasks/blob/master/basic-line.png)

It can be clearly observed that in states with low literacy rates, Females have the least literacy rate among the gender. This can be linked to gender discriminiation, child marriages.

<h2>The Process</h2>
<h3>Import the required Libraries</h3>

```Python
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
```
Pandas for manipulating dataFrames, plotly for plotting various graphs.

<h3> Read the CSV file and clean the data</h3>
```Python
census=pd.read_table('india-districts-census-2011.csv',sep=',') 
census.rename(columns={'State name':'state_name'},inplace=True)
new_columns=['state_name','Population','Literate','Households','Female_Literate','Male_Literate','Household_size_5_persons_Households','Household_size_6_8_persons_Households','Household_size_9_persons_and_above_Households']
census_trimmed=pd.DataFrame(census[new_columns])
```
load the CSV file and trim the columns to the ones needed for this analysis.

<h3>Create new columns for analysis</h3>

```Python
census_trimmed['Literacy_Rate']=(((census_trimmed.Literate)/(census_trimmed.Population))*100)
census_trimmed['Literate_Male']=(((census_trimmed.Male_Literate)/(census_trimmed.Literate))*100)
census_trimmed['Literate_Female']=(((census_trimmed.Female_Literate)/(census_trimmed.Literate))*100)
census_trimmed['house_hold_above_5_People']=(((census_trimmed.Household_size_5_persons_Households+census_trimmed.Household_size_6_8_persons_Households+census_trimmed.Household_size_9_persons_and_above_Households)/(census_trimmed.Households))*100)
```

Create columns which calculate the literacte rate and other metrics required for comparision and analysis.

<h3>Groupby state names</h3>

```Python
new_columns2=['state_name','Literacy_Rate','Literate_Male','Literate_Female','house_hold_above_5_People']
census_trimmed=pd.DataFrame(census_trimmed[new_columns2])
census_trimmed=census_trimmed.groupby('state_name',as_index=False).mean()
census_trimmed=census_trimmed.sort_values(by='Literacy_Rate',ascending=0)
census_trimmed.reset_index()
```
Remove uncessary columns, groupby state name and arrage in ascending order by literacy rate.

<h3>Creating Geographical map</h3>

![geomap using excel](https://github.com/Jagannath-Saragadam/gramenerTasks/blob/master/Screenshot%20(202).png)

This geographical map has been created using Gramener's resource (Source:https://gramener.com/map/)
<h3>Plot</h3>

```Python
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
```

<h2>Question 2: Find out most similar districts in Bihar and Tamil Nadu. Similarity can be based on any of the columns from the data.</h2>

To find out similar districts between Bihar and Tamil Nadu, I've taken each district from Bihar and compared it with every district of Tamil Nadu, found the ratio and allowed a maxium deviation of **+_5%**

<h3>Import the required Libraries</h3>

```Python
from __future__ import division
import pandas as pd
import statistics as st
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
```

<h3>Clean the data</h3>

```Python
census=pd.read_table('india-districts-census-2011.csv',sep=',') 
census.rename(columns={'State name':'state_name'},inplace=True)
census.rename(columns={'District name':'district_name'},inplace=True)
census_bihar=census.loc[(census.state_name=="BIHAR")]
census_tamilNadu=census.loc[(census.state_name=="TAMIL NADU")]
census_tamilNadu = census_tamilNadu.rename(columns={'district_name': 'tname'})
census_bihar.reset_index()
census_tamilNadu.reset_index()
```

<h3>Find similar districts</h3>

```Python
similar=[]
for index, row in census_bihar.iterrows():
    for index1,row1 in census_tamilNadu.iterrows():
        if 0.95<(census_bihar.Population[index]/census_tamilNadu.Population[index1])<1.05:
            similar.append({census_bihar.district_name[index]:census_bihar.Population[index],census_tamilNadu.tname[index1]:census_tamilNadu.Population[index1]})
````
**Output**

```
[{'Kancheepuram': 3998252, 'Pashchim Champaran': 3935042},
 {'Pashchim Champaran': 3935042, 'Vellore': 3936331},
 {'Sitamarhi': 3423574, 'Viluppuram': 3458873},
 {'Salem': 3482056, 'Sitamarhi': 3423574},
 {'Coimbatore': 3458045, 'Sitamarhi': 3423574},
 {'Chennai': 4646732, 'Madhubani': 4487379},
 {'Erode': 2251744, 'Supaul': 2229076},
 {'Dindigul': 2159775, 'Supaul': 2229076},
 {'Araria': 2811569, 'Tiruchirappalli': 2722290},
 {'Kishanganj': 1690400, 'Namakkal': 1726601},
 {'Kishanganj': 1690400, 'Nagapattinam': 1616450},
 {'Kishanganj': 1690400, 'Pudukkottai': 1618345},
 {'Kishanganj': 1690400, 'Thoothukkudi': 1750176},
 {'Katihar': 3071029, 'Madurai': 3038252},
 {'Katihar': 3071029, 'Tirunelveli': 3077233},
 {'Madhepura': 2001762, 'Virudhunagar': 1942288},
 {'Saharsa': 1900661, 'Virudhunagar': 1942288},
 {'Kanniyakumari': 1870374, 'Saharsa': 1900661},
 {'Krishnagiri': 1879809, 'Saharsa': 1900661},
 {'Darbhanga': 3937385, 'Kancheepuram': 3998252},
 {'Darbhanga': 3937385, 'Vellore': 3936331},
 {'Chennai': 4646732, 'Muzaffarpur': 4801062},
 {'Gopalganj': 2562012, 'Tiruvannamalai': 2464875},
 {'Cuddalore': 2605914, 'Gopalganj': 2562012},
 {'Gopalganj': 2562012, 'Tiruppur': 2479052},
 {'Siwan': 3330464, 'Viluppuram': 3458873},
 {'Salem': 3482056, 'Siwan': 3330464},
 {'Coimbatore': 3458045, 'Siwan': 3330464},
 {'Kancheepuram': 3998252, 'Saran': 3951862},
 {'Saran': 3951862, 'Vellore': 3936331},
 {'Vaishali': 3495021, 'Viluppuram': 3458873},
 {'Salem': 3482056, 'Vaishali': 3495021},
 {'Coimbatore': 3458045, 'Vaishali': 3495021},
 {'Begusarai': 2970541, 'Madurai': 3038252},
 {'Begusarai': 2970541, 'Tirunelveli': 3077233},
 {'Khagaria': 1666886, 'Namakkal': 1726601},
 {'Khagaria': 1666886, 'Nagapattinam': 1616450},
 {'Khagaria': 1666886, 'Pudukkottai': 1618345},
 {'Khagaria': 1666886, 'Thoothukkudi': 1750176},
 {'Bhagalpur': 3037766, 'Madurai': 3038252},
 {'Bhagalpur': 3037766, 'Tirunelveli': 3077233},
 {'Banka': 2034763, 'Virudhunagar': 1942288},
 {'Munger': 1367765, 'Sivaganga': 1339101},
 {'Munger': 1367765, 'Ramanathapuram': 1353445},
 {'Bhojpur': 2728407, 'Tiruchirappalli': 2722290},
 {'Bhojpur': 2728407, 'Cuddalore': 2605914},
 {'Buxar': 1706352, 'Namakkal': 1726601},
 {'Buxar': 1706352, 'Thoothukkudi': 1750176},
 {'Kaimur (Bhabua)': 1626384, 'Nagapattinam': 1616450},
 {'Kaimur (Bhabua)': 1626384, 'Pudukkottai': 1618345},
 {'Madurai': 3038252, 'Rohtas': 2959918},
 {'Rohtas': 2959918, 'Tirunelveli': 3077233},
 {'Aurangabad': 2540073, 'Tiruvannamalai': 2464875},
 {'Aurangabad': 2540073, 'Cuddalore': 2605914},
 {'Aurangabad': 2540073, 'Tiruppur': 2479052},
 {'Erode': 2251744, 'Nawada': 2219146},
 {'Dindigul': 2159775, 'Nawada': 2219146},
 {'Jamui': 1760405, 'Namakkal': 1726601},
 {'Jamui': 1760405, 'Thoothukkudi': 1750176},
 {'Arwal': 700843, 'The Nilgiris': 735394}]
 ```
