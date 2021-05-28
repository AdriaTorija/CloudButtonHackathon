import pandas as pd
import getOfficialData as getOData
#df= pd.DataFrame({'tweets':tweets,'time':time,'likes':likes})
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from lithops import Storage
from io import BytesIO
from collections import Counter
import matplotlib.pyplot as plt
import nltk


bucket='cloudbuttonhackathon'
def mostCommonWords(df,n):
    splitText = []
    for text in df["Text"]:
        for word in str(text).split():
            splitText.append(word)
        m = Counter(splitText).most_common(n)
    wDf= pd.DataFrame(m)
    wDf.set_index(0)[1].plot(kind="pie",subplots=True)

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
        "Positives":pos,
        "Neutrals":neu,
        "Negatives":neg,        
    }
    aux= pd.DataFrame.from_dict(dict,orient='index')
    aux.transpose()
    aux.plot(kind='bar',title="Feelings",subplots=True)
    print(aux.describe())
    

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
    
    #Most Retweets
    #print(df.describe())
    #ax=df["Retweets"].plot(kind='density',figsize=(14,6))
    #ax.axvline(df["Retweets"].mean(), color='red')
    #ax.axvline(df["Retweets"].median(), color='green')
    #print(mostRetweeted(df,4))
    
    #Feelings
    feelings(df)
   
    
    
    #MostCommonWords
    mostCommonWords(df,5)
    

    #MostCommonHashtags
    #y=mostCommonHashtags(df,5)
    #hDf=pd.DataFrame(y)
    #aux=hDf.set_index(0)[1].plot(kind="bar",subplots=True)
    
analysis()
print("End of analysis")
