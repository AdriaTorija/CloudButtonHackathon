import lithops
fexec = lithops.ServerlessExecutor()
from getWebdata import getWebsHtml
from lithops.multiprocessing import Pool

webs=['https://www.reddit.com/r/COVID19/','https://www.reddit.com/r/COVID19positive/','https://www.reddit.com/r/Coronavirus/']
    
for i in webs:
    fexec.call_async(getWebsHtml,i) 

from lithops import Storage

