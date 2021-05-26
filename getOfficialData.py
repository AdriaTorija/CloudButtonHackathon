import io
import tweepy
import pandas as pd
from lithops import Storage
import json

bucket='cloudbuttonhackathon'                  #Change this value if you want to change the storage bucket


def dataSearch(keysText,hashtag,number_of_tweets):                       #keys: String of the file with keys
    #Reading the keys for connection                #Hashtag: hashtag we want to search and save tweets without #
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
    for i in tweepy.Cursor(api.search,q=stringSearch,tweet_mode="extended",until="2021-05-22").items(number_of_tweets):
    #for i in tweepy.Cursor(api.search_30_day("CloudButton0",q=stringSearch,fromDate="2021-05-0",toDate="2021-05-12",maxResults=4)).items(number_of_tweets):
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
        
    #Storing Information
    storage = Storage()
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
    with open("proves.json", 'w') as f:
       f.write(json.dumps(dict))

    #inf = pd.DataFrame(dict, columns = ['User', 'Likes', 'Retweets', 'Date', 'Url', 'Location', 'Text', 'Hashtags', 'Verified'])
    #inf.to_csv('prova.csv')

    #storage.put_object(bucket,"dataTwitter.json",json.dumps(dict))
    #storage.put_object(bucket,"text.txt",str(tweets))
    storage.put_object(bucket, "prova.csv", io.StringIO(dict))
    


def main():
    dataSearch("keys.txt","Covid19",10)

if __name__ == "__main__":
    main()