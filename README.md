# api_faili
Konteinrs ar kuru augšuplādē .csv failus
Izmantota Phyton valoda un uvicorn serveris kurš klausās 8000 portu

Augšuplādi var izsaukt no komandrindas: curl -F "file=@sezona.csv" http://localhost:8000/uploadfile

Augšuplādējot failam tiek mainīts nosaukums, sākumā pievienojot datumu un laiku. Tas tiek darīts, lai būtu iespēja augšuplādēt daudzus vienādus failus (konteiners kurš apstrādā failus šo ņem vērā).

### Tiek pārbaudīts:
* faila tips: jābūt .csv
* faila izmērs: definēts konfig.py - FILE_SIZE

### konfigs satur:
* DATABASE_URI - datubāzes konkecija
* FAILU_FOLDERIS - folderis kurā tiek saglabati faili, šo nepieciešams piemapot kā volumi kopīgu ar konteineri kurša apstrādā failus
* FILE_SIZE - maksimālais faila izmērs
* CHUNK_SIZE - gabaliņi kādos tiek sadalīts fails glabājot

### Logi un Metrikas (definēts metrikas šim konteinerim, izsaucot auditāciju tiek palielinātas)
* metrika=6, apraksts='api_faili_web: Augšuplādēts fails par lielu'
* metrika=7, apraksts='api_faili_web: Atrasts nekortekts fails (ne .csv fails)'
* metrika=8, apraksts='api_faili_web: Augšuplādēts .csv fails'
* metrika=9, apraksts='api_faili_web: Augšuplādēts kļūdaina'
