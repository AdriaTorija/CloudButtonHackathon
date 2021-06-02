from nltk.util import pr
import numpy as np
import pandas as pd
import getOfficialData as getOData
#df= pd.DataFrame({'tweets':tweets,'time':time,'likes':likes})
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from lithops import Storage
from io import BytesIO
from collections import Counter
import matplotlib.pyplot as plt
from googletrans import Translator
import seaborn
import nltk
from lithops.multiprocessing import Pool
nltk.download('vader_lexicon')

bucket='cloudbuttonhackathon'
def mostCommonWords(df,n):
    splitText = []
    for text in df["Text"]:
        for word in str(text).split():
            splitText.append(word)
        m = Counter(splitText).most_common(n)
        print(m)
    #wDf= pd.DataFrame(m)
    #wDf.set_index(0)[1].plot(kind="pie",subplots=True)
    return pd.DataFrame(m)

def feelings(df):
    translator = Translator()
    analyzer = SentimentIntensityAnalyzer()
    pos, neg, neu = 0, 0, 0
    positive, neutral, negative = [], [], []
    for text in (df["Text"]):
        text=translator.translate(text,dest="en").text
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
    return pd.DataFrame([[key, dict[key]] for key in dict.keys()])
    

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
    fig, axs = plt.subplots(1, 3)
    #Most Retweets
    #print(df.describe())
    #ax=df["Retweets"].plot(kind='density',figsize=(14,6))
    #ax.axvline(df["Retweets"].mean(), color='red')
    #ax.axvline(df["Retweets"].median(), color='green')
    print(mostRetweeted(df,4))

    #Feelings
    feel = feelings(df)
    seaborn.barplot(x=0, y=1, data=feel, ax=axs[0])

    #MostCommonWords
    wDf = mostCommonWords(df,5)
    seaborn.barplot(x=0, y=1, data=wDf, ax=axs[1])
    axs[1].set(xlabel="Paraula", ylabel = "N vegades")

    #Users i retweets
    seaborn.scatterplot(x="User", y="Retweets", data=df, ax=axs[2])
    #plt.show()
    

    #MostCommonHashtags
    #y=mostCommonHashtags(df,5)
    #hDf=pd.DataFrame(y)
    #aux=hDf.set_index(0)[1].plot(kind="bar",subplots=True)


def main():
    with Pool() as pool:
        result=pool.starmap(analysis, [()])
    

    print('hola')
    
if __name__ == '__main__':
    main()
