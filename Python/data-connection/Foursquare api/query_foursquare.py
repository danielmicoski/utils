import json, requests
url = 'https://api.foursquare.com/v2/venues/explore'

params = dict(
  client_id='YTSZFGCMLMY5WO0ZPTYMQQFI40SISANJUR1MECUUMFVEUNYH',
  client_secret='FW3AZH1YEGX3LBEYFGESOXYU45UFV3UOL23V0TQTMNRFQX2C',
  v='20191128',
  #radius='10000',
  limit='2000',
  query='adidas',
  intent='global',
  #ll='34.398483,-94.39398',
  ll='28.4009598,-81.4646355'
)


resp = requests.get(url=url, params=params)
data = json.loads(resp.text)

w = open('data/teste_fq6.json','w')
w.write(str(data))
w.close()