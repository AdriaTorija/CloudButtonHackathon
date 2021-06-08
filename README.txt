# SD_CloudButtonHackathon
Practica2

Autors: 
Xavier Roca Canals
Adrià Rubio Busquets
Adrià Torija Ruiz

---------------------

GitHub: https://github.com/hatori9/CloudButtonHackathon

----------------------

La pràctica l’hem realitzat conjuntament, si ho poguéssim dividir d’alguna manera seria aquesta, 
encara que haguem participat tots en cada part: 
Xavier Roca Canals: Analitzar dades tweets i realitzar/proposar gràfiques per tweets i Reddit. 
Adrià Rubio Busquets: Agafar dades de Reddit i analitzar-les. 
Adrià Torija Ruiz: Configuració Lithops + Docker i agafar dades de tweets. 

----------------------

getTwitterOfficialData.py

En aquest primer fitxer (getTwitterOfficialData.py), el que busquem es extreure informació, en 
aquest cas tweets, de Twitter. 
Per aconseguir això, utilitzarem la llibreria tweepy. Aquesta ens permet accedir a la API de 
Twitter per realitzar aquesta recopilació. Els tweets que buscarem estaran relacionats amb el 
tema comentat i el idioma que ens centrarem serà l’anglès i l’espanyol. 

dataSearch(hashtag, number_of_tweets):

Funcionalitat: 
Ens connectarem a la API de twitter i buscarem tots els tweets amb els paràmetres comentats 
anteriorment (hashtags i nombre de tweets) i en idioma angles i espanyol. 
Per cada un dels tweets recollirem la següent informació: Usuari, Likes, Retweets, Data, Url, Text 
(Contingut del tweet), Hashtags i si l’usuari està verificat. 
Finalment, emmagatzemem aquesta informació en un csv al Cloud Object Storage del Cloud de 
IBM per tal d’analitzar-la posteriorment. 

------------------------

getWebdata.py

Per fer aquesta recerca utilitzarem la llibreria scrapy, una eina molt potent per 
rastrejar/analitzar webs. 
Scrapy utilitza les spiders per extreure tota aquesta informació. 

Get_past_date(str_days_ago): 
Funcionalitat: 
Canvia el format al tradicional de la data: día:mes:any 

Start_Request(): 
Funcionalitat: 
Fa una request amb el scrapy per cada url que hem escollit. Aquesta cridarà a la funció parse. 
A partir del link que li arriba tracta la seva informació, guardarem tota la informació que ens 
interessa i seguirem entrant als links que hi han dins d’aquesta url. 
Per indicar la profunditat de cerca dins d’un url estarà marcada per una variable maxdepth. 
Finalment, emmagatzemem aquesta informació en un csv al Cloud Object Storage del Cloud de 
IBM 

------------------------

twitterDataAnalysis.py

En aquest fitxer (twitterDataAnalysis.py), analitzarem de diferents maneres les dades 
emmagatzemades en el csv de twitter

mostCommonWords(df,n): 

Funcionalitat: 
A partir del text dels tweets, mirem quines són les paraules més utilitzades.

Feelings(df):

Funcionalitat: 
A partir del text dels tweets realitzarem un anàlisis de sentiment.

mostCommonHashtags(df,n) 

Funcionalitat: 
A partir del text dels tweets, mirem quines són les paraules més utilitzades. 

verifiedTweet(df) 

Funcionalitat: 
Comprovem quants usuaris estan o no verificats.
 
mostRetweetedInADay(df,date) 

Funcionalitat: 
Agafarem els cinc tweets amb més retweets de la data passada per paràmetre. 
A més farem una comparativa entre els url i els retweets que tenen. 
Per cada funció farem la seva gràfica.

--------------------------

webDataAnalysis.py

En aquest fitxer (webDataAnalysis), analitzarem de diferents maneres les dades 
emmagatzemades en el csv de reddit. Analitzarem cada url i mirarem quants comentaris i vots tenen en comparació amb la data que 
es van publicar. 

Feelings(df): 

Funcionalitat: 
A partir del text dels tweets realitzarem un anàlisis de sentiment. 

wordCounting(df): 

Funcionalitat: 
Segons paraules clau com: covid, virus, vacuna, positiu i hospital, mira quants cops surten en el 
text de cada post de Reddit, finalment es fa la Mitjana (alhora de fer els gràfics) amb el numero 
total dels posts.
 
Analysis():

Funcionalitat: 
Executa totes les funcions i crea les gràfiques corresponents. 

--------------------------

DeleteDataCloud.py

Fitxer per a esborrar els archius del cloud menys els keys.txt, el webs.csv i tweets.csv