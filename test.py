from lithops.executors import FunctionExecutor
from getWebdata import getWebsHtml
import lithops
import pandas as pd
from lithops import Storage
import tweepy
from lithops.multiprocessing import Pool
import scrapy
from scrapy import linkextractors
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

webs=['https://www.reddit.com/r/COVID19/']
web=['https://www.reddit.com/r/COVID19/','https://www.reddit.com/r/COVID19positive/','https://www.reddit.com/r/Coronavirus/']  

bucket='cloudbuttonhackathon'
storage=Storage()



def dataSearch(hashtag,number_of_tweets):                       #keys: String of the file with keys
    #Reading the keys for connection                #Hashtag: hashtag we want to search and save tweets without #
    storage = Storage()
    storage=Storage()
    f=storage.get_object(bucket,"keys.txt")
    keys= f.decode('ascii').split('\n')
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
    inf = pd.DataFrame(dict, columns = ['User', 'Likes', 'Retweets', 'Date', 'Url', 'Location', 'Text', 'Hashtags', 'Verified'])
    storage.put_object(bucket, "prova.csv", inf.to_csv(index=False))


#scrapy

bucket='cloudbuttonhackathon'                  #Change this value if you want to change the storage bucket
words= ['Covid', 'covid19', 'virus', 'Coronavirus', 'COVID-19', 'COVID', 'vaccine', 'Vaccine', 'positive', 'Positive', 'Hospital', 'hospital']
names=[]
linksss=[]
items = []

filenames=[]
commentarios=[]
votes=[]
dates=[]
texts=[]

class TestSpider(scrapy.Spider):
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
          callback="parse_item"
      )
  ]

  maxdepth = 1

  def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

  """ def parse_item(self, response):
        # The list of items that are found on the particular page
        
        # Only extract canonicalized and unique links (with respect to the current page)
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        # Now go through all the found links
        for link in links:
            # Check whether the domain of the URL of the link is allowed; so whether it is in one of the allowed domains
            is_allowed = False
            for allowed_domain in self.allowed_domains:
                if allowed_domain in link.url:
                    is_allowed = True
            # If it is allowed, create a new item and add it to the list of found items
            if is_allowed:
                item = DatabloggerScraperItem()
                item['url_from'] = response.url
                item['url_to'] = link.url
                items.append(item)
                linksss.append(link.url)
        for link_to_follow in items:
            yield scrapy.request(link_to_follow['url_from'], callback=self.parse)
                
        # Return all the found items
        #return items """

  def parse(self, response):
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
                dict={
                "URL":response.url,
                "Titles":titles, 
                "Texts": text[0],
                "Comments":comment,
                "Votes": vot[0],
                "Dates": date[0]
                }
                storage=Storage()
                storage.put_object(bucket, response.url, dict)
      # Update the print logic to show what page contain a link to the
      # current page, and what was the text of the link
      #print(depth, response.url, '<-', from_url, from_text, sep=' ')
      # Browse a tags only if maximum depth has not be reached
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
      
  """ def parse(self, response):
    # Do something useful/meaningful.
    self.logger.info("Following %s", response.url) 
    page = response.url.split("/")[-2]
    filename = f'{page}.html'
    #with open(filename, 'wb') as f:
    #   f.write(response.body)
    storage = Storage()
    print(filename)
    storage.put_object(bucket,filename,getText(response.body)) """

#process = CrawlerProcess()
#web=['https://www.reddit.com/r/COVID19/','https://www.reddit.com/r/COVID19positive/','https://www.reddit.com/r/Coronavirus/']  


 

def getWebsHtml():
    #TestSpider.start_urls=['https://www.reddit.com/r/COVID19/']     #Example
    process = CrawlerProcess()
    process.crawl(TestSpider)
    process.start() # the script will block here until the crawling is finished """
    storage=Storage()
    list=storage.list_keys(bucket)
    

    """ for a in list:
        num=[]
        name=a.split('.')[0]
        if name != 'lithops' and name != 'dataWEB':
          filenames.append(a)
          text=storage.get_object(bucket,a)
          texts.append(str(text))
          texto=str(text).split()
          i=0
          for b in words:
              y=0
              num.append(y)
              for c in texto:
                  if b == c:
                    y=y+1
                    num[i]=y
              i=i+1
          names.append(num) """
    
      
    dict={
        "URL":linksss,
        "Titles":filenames, 
        "Texts": texts,
        "Comments":commentarios,
        "Votes": votes,
        "Dates": dates
        }
    #print(dict)
    #print('\n\n\n\n\n')
    #list=storage.list_keys(bucket)
    #storage.delete_objects('cloudbuttonhackathon',list)

    #storage.put_object(bucket,"dataWEB.json",json.dumps(dict))
    inf = pd.DataFrame.from_dict(list)
    inf.to_csv("hola.csv", index=False)
    #storage.put_object(bucket, "data.csv", inf.to_csv(index=False))

    #pdOBJ = pd.read_json(storage.get_object(bucket, "dataWEB.json"), orient='index')
    #pdOBJ.to_csv('data.csv', index=False)


data= []

with Pool() as pool:
    result=pool.map(getWebsHtml,[data])

#pool.starmap(getWebsHtml(web))