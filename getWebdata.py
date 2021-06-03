import scrapy
import pandas as pd
import seaborn
import matplotlib.pyplot as plt
import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from lithops import Storage
from dateutil.relativedelta import relativedelta

bucket='cloudbuttonhackathon'                  #Change this value if you want to change the storage bucket
covid= ['Covid', 'covid19', 'Coronavirus', 'COVID-19', 'COVID']
virus = ['virus']
vacuna = ['vaccine', 'Vaccine', 'astrazeneca', 'AstraZeneca']
positiu = ['positive', 'Positive']
hospital = ['Hospital', 'hospital']
words = [covid, virus, vacuna, positiu, hospital] #list of related word about covid
names=[] #names 
linksss=[] #url 
filenames=[] #titles
commentarios=[] #comments
votes=[] #votes
dates=[] #dates
texts=[] #texts
cov=[]
vir=[]
pos=[]
vac=[]
hos=[]

def get_past_date(str_days_ago): #function to get the dates from strings like 1 hour ago
    TODAY = datetime.date.today()
    splitted = str_days_ago.split()
    if len(splitted) == 1 and splitted[0].lower() == 'today':
        return str(TODAY.isoformat())
    elif len(splitted) == 1 and splitted[0].lower() == 'yesterday':
        date = TODAY - relativedelta(days=1)
        return str(date.isoformat())
    elif splitted[1].lower() in ['hour', 'hours', 'hr', 'hrs', 'h']:
        date = datetime.datetime.now() - relativedelta(hours=int(splitted[0]))
        return str(date.date().isoformat())
    elif splitted[1].lower() in ['day', 'days', 'd']:
        date = TODAY - relativedelta(days=int(splitted[0]))
        return str(date.isoformat())
    elif splitted[1].lower() in ['wk', 'wks', 'week', 'weeks', 'w']:
        date = TODAY - relativedelta(weeks=int(splitted[0]))
        return str(date.isoformat())
    elif splitted[1].lower() in ['mon', 'mons', 'month', 'months', 'm']:
        date = TODAY - relativedelta(months=int(splitted[0]))
        return str(date.isoformat())
    elif splitted[1].lower() in ['yrs', 'yr', 'years', 'year', 'y']:
        date = TODAY - relativedelta(years=int(splitted[0]))
        return str(date.isoformat())
    elif splitted[1].lower() in ['min', 'm', 'minutes', 'minute']:
        date = TODAY - relativedelta(years=int(splitted[0]))
        return str(TODAY.isoformat())
    else:
        return "Wrong Argument format"

class TestSpider(scrapy.Spider): #main class scrppy
  name = "test" 

  allowed_domains = ['reddit.com']
  # The URLs to start with
  start_urls = ['https://www.reddit.com/r/COVID19/','https://www.reddit.com/r/COVID19positive/','https://www.reddit.com/r/Coronavirus/'] 
  # This spider has one rule: extract all (unique and canonicalized) links, follow them and parse them using the parse_items method
  rules = [
      Rule(
          LinkExtractor(
              canonicalize=True,
              unique=True
          ),
          follow=True,
          callback="parse"
      )
  ]

  maxdepth = 1

  def start_requests(self): #starts request from urls in start_urls
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

  def parse(self, response): #function to get all the information from the urls
      # Set default meta information for first page
      from_url = ''
      from_text = ''
      depth = 0;
      # Extract the meta information from the response, if any
      if 'from' in response.meta:
          from_url = response.meta['from']
      if 'text' in response.meta:
          from_text = response.meta['text']
      if 'depth' in response.meta:
          depth = response.meta['depth']
      
      
      aux=response.url.split('/')
      tema=''
      covid=False
      for i in aux:
            if i == 'COVID19' or i == 'COVID19positive' or i == 'Coronavirus':
                covid=True
            if i == 'comments' and covid == True:
                tema = 'comments'
      if tema == 'comments':
            auxx=False
            titulo = response.css('._eYtD2XCVieq6emjKBH3m::text').extract()
            titles = titulo[0]
            for i in filenames:
                if i == titles:
                    auxx=True
            if auxx==False:
                date = response.css('._3jOxDPIQ0KaOWpzvSQo-1s::text').extract()
                vot = response.css('._1rZYMD_4xY3gRcSS3p8ODO::text').extract()
                comments = response.css('.FHCV02u6Cp2zYL0fhQPsO::text').extract()
                text = response.css('._1qeIAgB0cPwnLhDF9XSiJM::text').extract()

                comment=comments[0].split(' ')[0]
                if vot[0] == "Vote":
                        vot[0]="0"
                realvot=vot[0]
                
                if realvot[-1] == "k":
                        a=realvot.replace('k', '')
                        realcom = float(a) * 1000
                        votes.append(realcom)
                else:
                    votes.append(realvot)

                if comment[-1] == "k":
                        a=comment.replace('k', '')
                        realcom = float(a) * 1000
                        commentarios.append(realcom)
                else:
                    commentarios.append(comment)

                date=get_past_date(date[0])
                
                linksss.append(response.url)
                texts.append(' '.join(text))
                filenames.append(titles)
                dates.append(date)
  
      if depth < self.maxdepth:
          a_selectors = response.xpath("//a")
          for selector in a_selectors:
              
              text = selector.xpath("text()").extract_first()
              link = selector.xpath("@href").extract_first()
              request = response.follow(link, callback=self.parse)
              # Meta information: URL of the current page
              request.meta['from'] = response.url
              
              # Meta information: text of the link
              request.meta['text'] = text
              
              # Meta information: depth of the link
              request.meta['depth'] = depth + 1
              
              """ storage.put_object(bucket,link,text) """

              yield request

def getWebsHtml(data):
    #TestSpider.start_urls=['https://www.reddit.com/r/COVID19/']     #Example
    process = CrawlerProcess()
    process.crawl(TestSpider)
    process.start() # the script will block here until the crawling is finished """
    storage=Storage()
    i=0
    for a in texts:
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
      
    dict={
        "URL":linksss,
        "Titles":filenames, 
        "Texts": texts,
        "Comments":commentarios,
        "Votes": votes,
        "Dates": dates,
        "Covid": cov,
        "Positive": pos,
        "Virus": vir,
        "Hospital": hos,
        "Vacuna": vac
        }

    inf = pd.DataFrame.from_dict(dict)
    inf.to_csv("data.csv", index=False)
    csv = pd.read_csv(r'data.csv')
    fig, axes = plt.subplots(1, 3)
    avg = csv.loc[:, ['Covid', 'Positive', 'Virus', 'Hospital', 'Vacuna']]
    seaborn.scatterplot(ax=axes[0], x="Dates", y="Comments", data=csv)
    axes[0].set_title("Comments")
    seaborn.scatterplot(ax=axes[1], x="Dates", y="Votes", data=csv)
    axes[1].set_title("Votes")
    avg.mean().plot(kind='bar', ax=axes[2], x=0, y=1)
    #axes[2].st_title("Average words")
    #seaborn.scatterplot(data=avg.mean())
    #axes[0].set_title("Covid")
    plt.show()
    storage.put_object(bucket, "data.csv", inf.to_csv(index=False))



      



