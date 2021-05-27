import pandas as pd
import getOfficialData as getOData
#df= pd.DataFrame({'tweets':tweets,'time':time,'likes':likes})
import nltk
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from lithops import Storage
from io import BytesIO


bucket='cloudbuttonhackathon'

def analysis():
    storage=Storage()
    data=storage.get_object(bucket,"prova.csv")
    df = pd.read_csv(BytesIO(data))
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
    print(pos)
    print(neg)
    print(neu)

 
def main():
    analysis()
    print("End of analysis")
if __name__ == "__main__":
    main()