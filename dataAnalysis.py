from nltk.util import pr
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from lithops import Storage
from io import BytesIO
from collections import Counter
import matplotlib.pyplot as plt
from googletrans import Translator
import seaborn
import nltk
from lithops.multiprocessing import Pool
from operator import itemgetter
from heapq import nlargest

bucket='cloudbuttonhackathon'

#Take the N most common words
def mostCommonWords(df,n):
    splitText = []
    for text in df["Text"]:
        for word in str(text).split():
            splitText.append(word)
        m = Counter(splitText).most_common(n)
        print(m)
    return m

#Sentiment analysis
def feelings(df,n):
    nltk.download('vader_lexicon')
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
    dict=[pos,neu,neg]

    return dict
    
#Take the N most common hashtags
def mostCommonHashtags(df,n):
    splitHash=[]
    for i in df["Hashtags"]:
        for word in str(i).split(','):
            if(word!='' and word!='nan'):
                splitHash.append(word.upper())
        m = Counter(splitHash).most_common(n)
    return m
    
#Counts how many tweets are made by veridied/not verified accounts
def verifiedTweet(df,n):
    yes = 0
    no = 0
    for verified in df["Verified"]:
        if verified:
            yes = yes +1
        else:
            no = no + 1

    dict=[yes,no]
    return dict

#Take the 5 most retweeted tweets according to the day passed by parameter
def mostRetweetedInADay(df,date):
    url = df[df['Date']==date]['Url']

    result = nlargest(5, enumerate(df[df['Date']==date]['Retweets']), itemgetter(1))
    urlList = []
    rt = []
    for value in result:
        urlList.append(url[value[0]])
        rt.append(value[1])

    dict = [urlList, rt]

    return dict


def main():

    storage=Storage()
    data=storage.get_object(bucket,"tweets.csv")
    df = pd.read_csv(BytesIO(data))
    fig, axs = plt.subplots(1, 6)  

    with Pool() as pool:
        mcW=pool.starmap(mostCommonWords,[(df,5)])
        mcH=pool.starmap(mostCommonHashtags, [(df,5)])
        #feel=pool.starmap(feelings, [(df,"")])
        veri=pool.starmap(verifiedTweet, [(df,"")])
        mrT = pool.starmap(mostRetweetedInADay, [(df, '2021-06-05')])

    #Url/Retweets plot
    seaborn.scatterplot(x="Url", y="Retweets", data=df, ax=axs[0])
    
    #MostCommonWord plot
    pdmcW = pd.DataFrame(mcW[0])
    seaborn.barplot(x=0, y=1, data=pdmcW, ax=axs[1])

    #MostCommonHashtag plot
    pdmcH = pd.DataFrame(mcH[0])
    seaborn.barplot(x=0, y=1, data=pdmcH, ax=axs[2])

    #SentimentAnalysis plot
    feel = feelings(df, "")
    #pdfeel = pd.DataFrame(feel)
    aux={
        "Positives":feel[0],
        "Neutrals":feel[1],
        "Negatives":feel[2],        
    }
    feel=pd.DataFrame(aux.items())
    seaborn.barplot(x=0, y=1, data=feel, ax=axs[3])
    
    #Verified plot
    aux={
         "Verified":veri[0][0],
         "NotVerified":veri[0][1]
    }
    pdverified=pd.DataFrame(aux.items())
    seaborn.barplot(x=0, y=1, data=pdverified, ax=axs[4])
    
    #mostRetweetedInADay plot
    mostRT={
         mrT[0][0][0]:mrT[0][1][0],
         mrT[0][0][1]:mrT[0][1][1],
         mrT[0][0][2]:mrT[0][1][2],
         mrT[0][0][3]:mrT[0][1][3],
         mrT[0][0][4]:mrT[0][1][4]
    }

    mostRTdf=pd.DataFrame(mostRT.items())
    seaborn.barplot(x=0, y=1, data=mostRTdf, ax=axs[5])
    plt.show()

if __name__ == '__main__':
    main()
