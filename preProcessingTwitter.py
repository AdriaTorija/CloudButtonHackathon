import lithops
from lithops import Storage
import json
import pandas as pd
from io import BytesIO

object_chunksize = 4*1024**2  # 4MB
bucket='cloudbuttonhackathon' 

#Convert all data to csv
def convert_to_csv(results):
    storage = Storage()
    for dict in results:
        inf = pd.DataFrame(dict, columns = ['User', 'Likes', 'Retweets', 'Date', 'Url', 'Text', 'Hashtags', 'Verified'])    
        nofile=1
        for i in storage.list_keys(bucket):
            if i == "tweets.csv":
                nofile=0
        if(nofile == 0):
            data=storage.get_object(bucket,"tweets.csv")
            df = pd.read_csv(BytesIO(data))
            result= df.append([inf])
            storage.put_object(bucket, "tweets.csv",result.to_csv(index=False))
        
        #If the file doesn't exist, we create it
        else:
            storage.put_object(bucket, "tweets.csv", inf.to_csv(index=False))
    
    return

#Convert the date to Year-Month-Day
def date(string):
    split_string = string.split()

    month = 0
    if(split_string[1] == "Jan"):
        month = 1
    elif(split_string[1] == "Feb"):
        month = 2
    elif(split_string[1] == "Mar"):
        month = 3
    elif(split_string[1] == "Apr"):
        month = 4
    elif(split_string[1] == "May"):
        month = 5
    elif(split_string[1] == "Jun"):
        month = 6
    elif(split_string[1] == "Jul"):
        month = 7
    elif(split_string[1] == "Aug"):
        month = 8
    elif(split_string[1] == "Sep"):
        month = 9
    elif(split_string[1] == "Oct"):
        month = 10
    elif(split_string[1] == "Nov"):
        month = 11
    elif(split_string[1] == "Dec"):
        month = 12

    return str(split_string[5]) + "-0" + str(month) + "-" + str(split_string[2])

#Get data from all files
def get_data(obj):
    data = obj.data_stream.read().splitlines()

    dict = {}
    tweets = []
    likes = []
    time = []
    hashtags = []
    urls = []
    names = []
    verified = []
    retweets = []

    #data_to_convert = data.split("\n")

    for d in data:
        
        i = json.loads(d)

        tweets.append(i["full_text"])
        likes.append(i["favorite_count"])
        time.append(date(str(i["created_at"])))
        aux = ""
        for j in i["entities"]["hashtags"]:
            aux = aux + j["text"] + ","
        hashtags.append(aux)
        urls.append(f"https://twitter.com/user/status/"+str(i["id"]))
        names.append(i["user"]["screen_name"])
        verified.append(i["user"]["verified"])
        retweets.append(i["retweet_count"])
        dict={
            "User":names,
            "Likes":likes,
            "Retweets":retweets,
            "Date":time,
            "Url":urls,
            "Text":tweets,
            "Hashtags":hashtags,
            "Verified":verified,
        }

    return dict


fexec = lithops.FunctionExecutor()
iterdata = [bucket+'/Covid/', bucket+'/CovidVaccine/', bucket+'/SARS-CoV-2/']
fexec.map_reduce(get_data, iterdata, convert_to_csv)
result = fexec.get_result()



