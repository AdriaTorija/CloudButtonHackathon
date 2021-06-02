import io
import tweepy
import pandas as pd
from lithops import Storage
import json
import csv
bucket='cloudbuttonhackathon'                  #Change this value if you want to change the storage bucket



def dataSearch(hashtag,number_of_tweets):                       #keys: String of the file with keys
    #Reading the keys for connection                #Hashtag: hashtag we want to search and save tweets without #
    storage = Storage()
    storage=Storage()
    
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
    lang= "lang:es"

    stringSearch="#"+hashtag + lang 
    print("Searching: "+stringSearch)
    for i in tweepy.Cursor(api.search,q=stringSearch,tweet_mode="extended").items(number_of_tweets):
        print(i)
        print("HOLA")
        tweets.append(i.full_text)
        likes.append(i.favorite_count)
        time.append(str(i.created_at))

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
        "Location":geo,
        "Text":tweets,
        "Hashtags":hashtags,
        "Verified":verified,
    }
    
    print(dict)
    inf = pd.DataFrame(dict, columns = ['User', 'Likes', 'Retweets', 'Date', 'Url', 'Location', 'Text', 'Hashtags', 'Verified'])
    storage.put_object(bucket, "prova.csv", inf.to_csv(index=False))


    #storage.put_object(bucket,"dataTwitter.json",json.dumps(dict))
    #storage.put_object(bucket,"text.txt",str(tweets)

#dataSearch("Covid19",5)