import requests
import os
import json
URL_BASE="https://api.pokemontcg.io/v1"
r=requests.get(URL_BASE+"/cards")
if r.status_code==200:
	doc=r.json()
	for i in doc["cards"]:
		try:
			print("Nombre:",i["name"],"HP:",i["hp"])
		except:
			print("Nombre:",i["name"])