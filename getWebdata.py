import scrapy
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from lithops import Storage
from dateutil.relativedelta import relativedelta

bucket='cloudbuttonhackathon'                  #Change this value if you want to change the storage bucket
names=[] #names 
linksss=[] #url 
filenames=[] #titles
commentarios=[] #comments
votes=[] #votes
dates=[] #dates
texts=[] #texts

def get_past_date(str_days_ago): #function to transform "1 hour/month/year" to formal date
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
      
      #get comment section
      aux=response.url.split('/')
      tema=''
      covid=False
      #prove that the comment section talks about Covid
      for i in aux:
            if i == 'COVID19' or i == 'COVID19positive' or i == 'Coronavirus':
                covid=True
            if i == 'comments' and covid == True:
                tema = 'comments'
      #if the link is a comment section
      if tema == 'comments':
            #get all the information from the links
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
  
      if depth < self.maxdepth: #go to the next link
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

              yield request

if __name__ == '__main__':
    #crawling process
    process = CrawlerProcess()
    process.crawl(TestSpider)
    process.start() # the script will block here until the crawling is finished """
    storage=Storage()
      
    dict={
        "URL":linksss,
        "Titles":filenames, 
        "Text": texts,
        "Comments":commentarios,
        "Votes": votes,
        "Dates": dates
        }

    #store csv into the cloud
    inf = pd.DataFrame(dict, columns=['URL', 'Titles', 'Text', 'Comments', 'Votes', 'Dates'])
    storage.put_object(bucket, "webs.csv", inf.to_csv(index=False))
    
    


      



