import io
import tweepy
import pandas as pd
from lithops import Storage
import json

bucket='cloudbuttonhackathon'                  #Change this value if you want to change the storage bucket


def dataSearch(keysText,hashtag,number_of_tweets):                       #keys: String of the file with keys
    #Reading the keys for connection                #Hashtag: hashtag we want to search and save tweets without #
    print("Keys:\n"+keysText)
    keys= open(keysText,'r').read().splitlines()
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
    lang= " lang:en OR lang:ca"

    stringSearch="#"+hashtag + lang 
    print("Searching: "+stringSearch)
    #for i in tweepy.Cursor(api.search,q=stringSearch,tweet_mode="extended",until="2021-05-22").items(number_of_tweets):
    for i in tweepy.Cursor(api.search_30_day("CloudButton0",q=stringSearch,fromDate="2021-05-0",toDate="2021-05-12",maxResults=4)).items(number_of_tweets):
        tweets.append(i.full_text)
        likes.append(i.favorite_count)
        time.append(str(i.created_at))
        print(i.created_at)
        for j in i.entities["hashtags"]:
            hashtags.append(j["text"])
        urls.append(f"https://twitter.com/user/status/{i.id}")
        geo.append(i.geo)
        names.append(i.user.screen_name)
        verified.append(i.user.verified)
        if i.user.verified :
            totalVerifiedUsers += 1
        retweets.append(i.retweet_count)
        
    #Storing Information
    storage = Storage()
    dict={
        "name":names,
        "likes":likes,
        "retweets":retweets,
        "time":time,
        "urls":urls,
        "geo":geo,
        "tweets":tweets,
        "hashtags":hashtags,
        "verified":verified,
        "TotalverifiedUsers":totalVerifiedUsers,
    }
    with open("proves.json", 'w') as f:
       f.write(json.dumps(dict))
    print(dict)
    #storage.put_object(bucket,"dataTwitter.json",json.dumps(dict))
    #storage.put_object(bucket,"text.txt",str(tweets))
    


def main():
    dataSearch("keys.txt","Covid19",4)
    print("gg")

if __name__ == "__main__":
    main()