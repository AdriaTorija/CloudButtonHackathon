from os import link
import lithops
from lithops import Storage
import json
import pandas as pd
import datetime
from io import BytesIO
from dateutil.relativedelta import relativedelta

object_chunksize = 4*1024**2  # 4MB
bucket='cloudbuttonhackathon' 

#Convert all data to csv
def convert_to_csv(results):
    storage = Storage()
    for dict in results:
        inf = pd.DataFrame(dict, columns = ['URL', 'Titles', 'Text', 'Comments', 'Votes', 'Dates'])    
        nofile=1
        for i in storage.list_keys(bucket):
            if i == "webs.csv":
                nofile=0
        if(nofile == 0):
            data=storage.get_object(bucket,"webs.csv")
            df = pd.read_csv(BytesIO(data))
            result= df.append([inf])
            storage.put_object(bucket, "webs.csv",result.to_csv(index=False))
        
        #If the file doesn't exist, we create it
        else:
            storage.put_object(bucket, "webs.csv", inf.to_csv(index=False))
    
    return

#function to transform "1 hour/month/year" to formal date
def get_past_date(str_days_ago):
    TODAY = datetime.date.today()
    splitted = str_days_ago.split()
    if len(splitted) == 1 and splitted[0].lower() == 'today':
        return str(TODAY.isoformat())
    elif len(splitted) == 1 and splitted[0].lower() == 'yesterday':
        date = TODAY - relativedelta(days=1)
        return str(date.isoformat())
    elif splitted[1].lower() in ['hour', 'hours', 'hr', 'hrs', 'h']:
        date = datetime.datetime.now() - relativedelta(hours=int(splitted[0]))
        return str(date.date().isoformat())
    elif splitted[1].lower() in ['day', 'days', 'd']:
        date = TODAY - relativedelta(days=int(splitted[0]))
        return str(date.isoformat())
    elif splitted[1].lower() in ['wk', 'wks', 'week', 'weeks', 'w']:
        date = TODAY - relativedelta(weeks=int(splitted[0]))
        return str(date.isoformat())
    elif splitted[1].lower() in ['mon', 'mons', 'month', 'months', 'm']:
        date = TODAY - relativedelta(months=int(splitted[0]))
        return str(date.isoformat())
    elif splitted[1].lower() in ['yrs', 'yr', 'years', 'year', 'y']:
        date = TODAY - relativedelta(years=int(splitted[0]))
        return str(date.isoformat())
    elif splitted[1].lower() in ['min', 'm', 'minutes', 'minute']:
        date = TODAY - relativedelta(years=int(splitted[0]))
        return str(TODAY.isoformat())
    else:
        return "Wrong Argument format"

#Get data from all files
def get_data(obj):
    data = obj.data_stream.read().splitlines()

    dict = {}
    linksss=[] #url 
    filenames=[] #titles
    commentarios=[] #comments
    votes=[] #votes
    dates=[] #dates
    texts=[] #texts
    

    #data_to_convert = data.split("\n")

    for d in data:
        
        i = json.loads(d)

        linksss.append(i["URL"])
        filenames.append(i["Titles"])
        texts.append(i["Text"])
        commentarios.append(i["Comments"])
        votes.append(i["Votes"])
        dates.append(get_past_date(str(i["Dates"])))
            
    dict={
        "URL":linksss,
        "Titles":filenames, 
        "Text": texts,
        "Comments":commentarios,
        "Votes": votes,
        "Dates": dates
        }

    return dict


fexec = lithops.FunctionExecutor()
iterdata = [bucket+'/COVID19/', bucket+'/COVID19Positive/', bucket+'/Coronavirus/']
fexec.map_reduce(get_data, iterdata, convert_to_csv)
result = fexec.get_result()
