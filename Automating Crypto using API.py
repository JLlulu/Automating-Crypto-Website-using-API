#!/usr/bin/env python
# coding: utf-8

# ## Test API

# In[2]:


from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'5000',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'ad83eea7-084e-4cf6-8518-0a38ea7f3b06',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)


# In[3]:


import pandas as pd

pd.set_option('display.max_columns',None)


# In[4]:


#to normalize the data and make it clear in a dataframe
df=pd.json_normalize(data['data'])
df['timestamp']=pd.to_datetime('now')
df


# ## Define function to get crypo price every 60 secs

# In[17]:



def api_runner():
    global df
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'start':'1',
      'limit':'15',
      'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': 'ad83eea7-084e-4cf6-8518-0a38ea7f3b06',
    }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      #print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
    
    df=pd.json_normalize(data['data'])
    df['timestamp']=pd.to_datetime('now')
    df
    
    if not os.path.isfile(r'C:\Users\Steph\OneDrive\桌面\Python for Financial Analysis and Algorathm Trading\API.csv'):
        df.to_csv(r'C:\Users\Steph\OneDrive\桌面\Python for Financial Analysis and Algorathm Trading\API.csv',header='column_names')
    else:
        df.to_csv(r'C:\Users\Steph\OneDrive\桌面\Python for Financial Analysis and Algorathm Trading\API.csv',mode='a',header=False)


# In[43]:


import os
from time import time
from time import sleep

for i in range(333):
    api_runner()
    print('API Runner completed')
    sleep(60)#sleep for 1 minute
exit()


# In[44]:


#save all crypto price to csv file
df72=pd.read_csv(r'C:\Users\Steph\OneDrive\桌面\Python for Financial Analysis and Algorathm Trading\API.csv')
df72


# ## Data Cleaning and transforming

# In[45]:


#first get a glance at the newest crypto info
df


# In[46]:


pd.set_option('display.float_format',lambda x:'%.5f'%x)


# In[47]:


df


# In[48]:


df2=df.groupby('name',sort=False)[['quote.USD.percent_change_1h','quote.USD.percent_change_24h','quote.USD.percent_change_7d','quote.USD.percent_change_30d','quote.USD.percent_change_60d','quote.USD.percent_change_90d']].mean()
df2


# In[49]:


df3=df2.stack()
df3


# In[50]:


df4=df3.to_frame(name='values')
df4


# In[51]:


df5=df4.reset_index()
df5


# In[52]:


df6=df5.rename(columns={'level_1':'percent_change'})
df6


# In[53]:


df6['percent_change']=df6['percent_change'].replace(['quote.USD.percent_change_1h','quote.USD.percent_change_24h','quote.USD.percent_change_7d','quote.USD.percent_change_30d','quote.USD.percent_change_60d','quote.USD.percent_change_90d'],['1h','24h','7d','30d','60d','90d'])


# ## Visualize crypto price percentage change

# In[33]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[39]:


sns.catplot(x='percent_change',y='values',hue='name',data=df6,kind='point')


# In[54]:


df7=df72[['name','quote.USD.price','timestamp']]
df7=df7.query('name=="Bitcoin"')
df7


# In[56]:


sns.lineplot(x='timestamp',y='quote.USD.price',data=df7)
plt.xticks([])
plt.show()


# In[ ]:




