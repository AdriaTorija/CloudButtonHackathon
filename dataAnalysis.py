import pandas as pd
import getOfficialData as getOData
#df= pd.DataFrame({'tweets':tweets,'time':time,'likes':likes})
import nltk
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from lithops import Storage
from io import BytesIO
from collections import Counter
bucket='cloudbuttonhackathon'
def mostCommonWords(df,n):
    splitText = []
    print(df)
    for text in df["Text"]:
        for word in str(text).split():
            splitText.append(word)
        m = Counter(splitText).most_common(n)
    return m

def feelings(df):
    analyzer = SentimentIntensityAnalyzer()
    pos, neg, neu = 0, 0, 0
    positive, neutral, negative = [], [], []
    for text in (df["Text"]):
        vs = analyzer.polarity_scores(str(text))
    #polary = analyzer.polarity_scores()
        if vs['compound'] >= 0.4:
            pos += 1
            if (text) not in positive:
                positive.append(text)
        elif vs['compound'] < 0.4 and vs['compound'] > -0.4:
            neu += 1
            if (text) not in neutral:
                neutral.append((text))
        else:
            neg += 1
            if (text) not in negative:
                negative.append(text)
  
    dict={
        "Positives":positive,
        "Neutrals":neutral,
        "Negatives":negative,        
    }
    return dict

def mostCommonHashtags(df,n):
    splitHash=[]
    for i in df["Hashtags"]:
        for word in str(i).split(','):
            if(word!='' and word!='nan'):
                splitHash.append(word.upper())
        m = Counter(splitHash).most_common(n)
    return m

def mostRetweeted(df,n):
    return max(df["Retweets"])

def verifiedTweet(df):
    i=0
    x=[]
    for j in df["Verified"]:
        
        if not j:
            x.append(df.loc[[i]])
        i = i+1
    return x
            
def analysis():
    storage=Storage()
    data=storage.get_object(bucket,"prova.csv")
    df = pd.read_csv(BytesIO(data))
    
analysis()
print("End of analysis")
