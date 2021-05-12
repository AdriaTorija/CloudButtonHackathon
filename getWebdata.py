import scrapy

class PostsSpider(scrapy.Spider):
    scrapy.Spider.name= 'posts'
    start_urls = [
        'https://blog.scrapinghub.com/page1/'
        'https://blog.scrapinghub.com/page2/'
    ]

    def parse(self, response):
        page = response.url.split('/')[-1]
        filename = ' posts-%s.html' % page
        with open(filename, 'wb') as f :
            f.write(response.body)
