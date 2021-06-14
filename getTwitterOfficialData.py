import io
from re import S
import tweepy
import pandas as pd
from lithops import Storage
from lithops.multiprocessing import Pool
from io import BytesIO
import json
from datetime import datetime

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
    tweets = []

    #Substraction of information
    lang= " lang:es OR lang:en"

    stringSearch="#"+hashtag + lang 
    print("Searching: "+stringSearch)
    for i in tweepy.Cursor(api.search,q=stringSearch,tweet_mode="extended").items(number_of_tweets):
        info = i._json
        tweets.append(json.dumps(info))

    data = str(datetime.now())
    nom = hashtag + "/" + data
    storage.put_object(bucket, nom, '\n'.join(tweets))

def main():
    with Pool() as pool:
        result=pool.starmap(dataSearch,[("Covid19",80), ("SARS-CoV-2",80),("CovidVaccine",80)])
    #dataSearch("Covid19", 5)
    
if __name__ == '__main__':
    main()