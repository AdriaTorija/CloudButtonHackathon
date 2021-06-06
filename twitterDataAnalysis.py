from nltk.util import pr
import pandas as pd
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
    return m

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

def main():

    storage=Storage()
    data=storage.get_object(bucket,"tweets.csv")
    df = pd.read_csv(BytesIO(data))
    fig, axs = plt.subplots(1, 5)
    

    with Pool() as pool:
        mcW=pool.starmap(mostCommonWords,[(df,5)])
        mcH=pool.starmap(mostCommonHashtags, [(df,5)])
        feel=pool.starmap(feelings, [(df,"")])
        veri=pool.starmap(verifiedTweet, [(df,"")])

    seaborn.scatterplot(x="User", y="Retweets", data=df, ax=axs[0])
    pdmcW = pd.DataFrame(mcW[0])
    seaborn.barplot(x=0, y=1, data=pdmcW, ax=axs[1])
    pdmcH = pd.DataFrame(mcH[0])
    seaborn.barplot(x=0, y=1, data=pdmcH, ax=axs[2])

    aux={
        "Positives":feel[0][0],
        "Neutrals":feel[0][1],
        "Negatives":feel[0][2],        
    }
    feel=pd.DataFrame(aux.items())
    seaborn.barplot(x=0, y=1, data=feel, ax=axs[3])
    
    aux={
         "Verified":veri[0][0],
         "NotVerified":veri[0][1]
    }
    pdverified=pd.DataFrame(aux.items())
    seaborn.barplot(x=0, y=1, data=pdverified, ax=axs[4])
    plt.show()

    print('hola')
    
if __name__ == '__main__':
    main()
