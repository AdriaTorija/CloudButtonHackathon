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
aquest cas tweets, de Twitter. Per aconseguir això, utilitzarem la llibreria tweepy. Aquesta ens permet accedir a la API de 
Twitter per realitzar aquesta recopilació. Els tweets que buscarem estaran relacionats amb el 
tema comentat i el idioma que ens centrarem serà l’anglès i l’espanyol. 
 

dataSearch(hashtag, number_of_tweets):

Funcionalitat: 
Ens connectarem a la API de twitter i buscarem tots els tweets amb els paràmetres comentats 
anteriorment (hashtags i nombre de tweets) i en idioma angles i espanyol. 
Guardarem tota la informació de cada tweet. Per guardar-ho en el Cloud ho farem de la següent 
manera: 
nom_hashtag/data_de_la_cerca 
On nom_hashtag, serà el hashtag pel qual buscarem tweets i data_de_la_cerca el fitxer on 
deixarem tots els tweets en aquella cerca d’aquest hashtag.

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

Parse():
 
Funcionalitat: 
Obté tota la informació que volem de les url dels posts de Reddit. 

------------------------

preProcessing.py

En aquest fitxer (preProcessing.py), convertirem tots els fitxers guardats anteriorment de twitter 
en un únic csv (tweets.csv). D’on finalment, en la última etapa farem els gràfics. 

Convert_to_csv(results): 

Funcionalitat: 
Per cada diccionari dins d’aquest resultat guardarem aquesta informació dins del csv. Abans 
mirarem si el fitxer tweets.csv ja està creat, de tal manera que puguem escriure tots els tweets. 

Date(string): 

Funcionalitat: 
A partir del string rebut amb la data en la que es guarda el json, el convertim en el format que 
nosaltres volem, és a dir, Any-Mes-Dia. 

Get_data(obj): 
 
Funcionalitat: 
Per cada fitxer que rebem agafarem la informació que ens interessa per afegir-la en un diccionari 
i com hem comentat abans, per tal d’afegir-la al csv en una altra funció. Els valors que agafarem 
són: Users, Likes, Retweets, Date, Url, Text, Hashtags i Verified. En el stage 3 realitzarem 
diferents anàlisi i gràfiques sobre aquestes dades. 

------------------------

preProcessingWeb.py

En aquest fitxer (preProcessingWeb.py), convertirem tots els fitxers guardats anteriorment de 
Reddit en un únic csv (webs.csv). D’on finalment, en la última etapa farem els gràfics. 

Convert_to_csv(results): 

Funcionalitat: 
Per cada diccionari dins d’aquest resultat guardarem aquesta informació dins del csv. Abans 
mirarem si el fitxer webs.csv ja està creat, de tal manera que puguem escriure tots els posts de 
reddit. 

Get_past_date(str_days_ago): 

Funcionalitat: 
Canvia el format al tradicional de la data: día:mes:any 

Get_data(obj): 

Funcionalitat: 
Per cada diccionari dins d’aquest resultat guardarem aquesta informació dins del csv. Abans 
mirarem si el fitxer webs.csv ja està creat, de tal manera que puguem escriure tots els posts de 
reddit.

------------------------

twitterDataAnalysis.ipnyb

Dins d’aquest fitxer (twitterDataAnalysis.ipnyb) trobarem el anàlisi i les gràfiques per al fitxer 
csv final de twitter (tweets.csv) 

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

webDataAnalysis.ipnyb

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

--------------------------

DeleteDataCloud.py

Fitxer per a esborrar els archius del cloud menys els keys.txt, el webs.csv i tweets.csv