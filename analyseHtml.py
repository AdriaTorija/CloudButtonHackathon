from lithops import Storage, storage
bucket='cloudbuttonhackathon'   
storage = Storage()
from bs4 import BeautifulSoup

def getText(htmlfile):
    #soup = BeautifulSoup(storage.get_object(bucket,a))     #Per agafar els html
    soup=BeautifulSoup(htmlfile)
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    #print(text)
    return text

#keys=storage.list_keys(bucket)
#for a in keys:
#  getText(a)
