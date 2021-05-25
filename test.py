import json, os
import lithops
import pandas as pd
from lithops import Storage
fexec = lithops.ServerlessExecutor()
from getWebdata import getWebsHtml
from lithops.multiprocessing import Pool
from lithops import FunctionExecutor
webs=['https://www.reddit.com/r/COVID19/']
web=['https://www.reddit.com/r/COVID19/','https://www.reddit.com/r/COVID19positive/','https://www.reddit.com/r/Coronavirus/']  

bucket='cloudbuttonhackathon'
storage=Storage()
#for i in storage.list_keys(bucket):
#    storage.delete_object(bucket,i)
data=[]
#for i in web:

with Pool() as pool:
    result = pool.map(getWebsHtml, webs)
    print(result)


#pdOBJ = pd.read_json(storage.get_object(bucket, "dataWEB.json"), orient='index')
#pdOBJ.to_csv('data.csv', index=False)

