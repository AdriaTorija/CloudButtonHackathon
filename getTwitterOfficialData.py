import io
from re import S
import tweepy
import pandas as pd
from lithops import Storage
from lithops.multiprocessing import Pool
from io import BytesIO

bucket='cloudbuttonhackathon'                  #Change this value if you want to change the storage bucket


#Search all tweets according to the HASHTAG
def dataSearch(hashtag,number_of_tweets):                       #keys: String of the file with keys
    #Reading the keys for connection                #Hashtag: hashtag we want to search and save tweets without #
    storage = Storage()
    
    f=storage.get_object(bucket,"keys.txt")

    keys= f.decode('ascii').split('\n')
   
    consumer_key=keys[0]
    consumer_secret=keys[1]
    access_token= keys[2]
    access_token_secret= keys[3]
    

    #Connecting with the cloud
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    api=tweepy.API(auth)


    #information we want to substract:
    dict = {}
    tweets = []
    likes = []
    time = []
    hashtags = []
    urls = []
    names = []
    totalVerifiedUsers = 0
    verified = []
    geo = []
    retweets = []
    #Substraction of information
    lang= " lang:es OR lang:en"

    stringSearch="#"+hashtag + lang 
    print("Searching: "+stringSearch)
    for i in tweepy.Cursor(api.search,q=stringSearch,tweet_mode="extended").items(number_of_tweets):
        tweets.append(i.full_text)
        likes.append(i.favorite_count)
        allTime = str(i.created_at).split()
        time.append(allTime[0])
        aux = ""
        for j in i.entities["hashtags"]:
            aux = aux + j["text"] + ","
        hashtags.append(aux)
        urls.append(f"https://twitter.com/user/status/{i.id}")
        geo.append(i.geo)
        names.append(i.user.screen_name)
        verified.append(i.user.verified)
        retweets.append(i.retweet_count)
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
    inf = pd.DataFrame(dict, columns = ['User', 'Likes', 'Retweets', 'Date', 'Url', 'Text', 'Hashtags', 'Verified'])    
    
    #If the file exists, we add the information at the end
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

def main():
    with Pool() as pool:
        result=pool.starmap(dataSearch,[("Covid19",80), ("SARS-CoV-2",80),("CovidVaccine",80)])
    
if __name__ == '__main__':
    main()