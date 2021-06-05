import seaborn
import pandas as pd
import matplotlib.pyplot as plt
import statistics
import nltk
from lithops import Storage
from lithops.multiprocessing import Pool
#from dataAnalysis import feelings
from io import BytesIO
from nltk.util import pr
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from googletrans import Translator

def feelings(df,n):
    nltk.download('vader_lexicon')
    translator = Translator()
    analyzer = SentimentIntensityAnalyzer()
    pos, neg, neu = 0, 0, 0
    positive, neutral, negative = [], [], []
    for text in (df["Text"]):
        aux=text
        try:
            text=translator.translate(text,dest="en").text
        except:
            text=aux
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

def WordCounting(df,n): 
    covid= ['Covid', 'covid19', 'Coronavirus', 'COVID-19', 'COVID']
    virus = ['virus']
    vacuna = ['vaccine', 'Vaccine', 'astrazeneca', 'AstraZeneca']
    positiu = ['positive', 'Positive']
    hospital = ['Hospital', 'hospital']
    cov=[]
    vir=[]
    pos=[]
    vac=[]
    hos=[]
    texts=df["Text"]
    i=0
    for a in texts: #get common words
            texto=a.split()
            cov.append(0)
            vir.append(0)
            pos.append(0)
            vac.append(0)
            hos.append(0)
            for b in texto:
                if b in covid:
                    cov[i]=cov[i]+1 
                if b in virus:
                    vir[i]=vir[i]+1 
                if b in positiu:
                    pos[i]=pos[i]+1
                if b in vacuna:
                    vac[i]=vac[i]+1 
                if b in hospital:
                    hos[i]=hos[i]+1                  
            i=i+1
    words=[cov,pos,vir,hos,vac]
    return words

def Analysis():
    storage=Storage()
    bucket='cloudbuttonhackathon'
    

    data=storage.get_object(bucket, "web.csv")
    csv = pd.read_csv(BytesIO(data))
    with Pool() as pool:
        list=pool.starmap(WordCounting,[(csv,"")])
        #feel=pool.starmap(feelings, [(csv,"")])
    
    dict={
            "Covid": statistics.mean(list[0][0]),
            "Positive": statistics.mean(list[0][1]),
            "Virus": statistics.mean(list[0][2]),
            "Hospital": statistics.mean(list[0][3]),
            "Vacuna": statistics.mean(list[0][4])
            }

    fig, axes = plt.subplots(1, 4)
    #get comments/dates plot
    seaborn.scatterplot(ax=axes[0], x="Dates", y="Comments", data=csv)
    axes[0].set_title("Comments")
     #get votes/dates plot
    seaborn.scatterplot(ax=axes[1], x="Dates", y="Votes", data=csv)
    axes[1].set_title("Votes")
    words=pd.DataFrame(dict.items())
     #get average words plot
    seaborn.barplot(ax=axes[2], x=0, y=1, data=words)
    axes[2].set_title("Average words")
    feel=feelings(csv,"")
    pd.DataFrame(feel)
    aux={
        "Positives":feel[0],
        "Neutrals":feel[1],
        "Negatives":feel[2],        
    }
    feeel=pd.DataFrame(aux.items())
     #get feelings plot
    seaborn.barplot(ax=axes[3], x=0, y=1, data=feeel)
    axes[3].set_title("Feels")
    #axes[2].st_title("Average words")
    #seaborn.scatterplot(data=avg.mean())
    #axes[0].set_title("Covid")
    plt.show()


if __name__ == '__main__':
   Analysis()