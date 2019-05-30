import requests
import os
import json
URL_BASE="https://api.clashroyale.com/v1/"
key=os.environ["keyroyale"]
equipo=input("¿Que equipo quieres buscar?: ")
payload={"name":equipo}
h={"Accept":"application/json","authorization":"Bearer %s"%key}
r=requests.get(URL_BASE+"clans",headers=h,params=payload)
doc=r.json()
print("Nombre de clanes:")
for i in doc["items"]:
	print(i["name"])
