from flask import Flask, render_template, request, abort
import requests
import os
import json
app = Flask(__name__)
URL_BASE="https://api.pokemontcg.io/v1/"
URL_BASE2="https://api.clashroyale.com/v1/"
key="asdasd"

@app.route('/',methods=['GET'])
def inicio():
	return render_template("index.html")

@app.route('/pokemontcg',methods=['GET'])
@app.route('/pokemontcg/<id>',methods=['GET'])
def cartas(id=1):
	payload={"page": id,"pageSize":40}
	r=requests.get(URL_BASE+"cards",params=payload)
	if r.status_code==200:
		doc=r.json()
		listaimagenes=[]
		for i in doc["cards"]:
			listaimagenes.append(i["imageUrlHiRes"])
		return render_template("pokemon.html",listaimagenes=listaimagenes,id=int(payload["page"]))
	else:
		abort(404)

@app.route('/pokemontcg/filtro',methods=['GET','POST'])
def filtro():
	datos=request.form.get("Carta")
	payload={"name": datos}
	r=requests.get(URL_BASE+"cards",params=payload)
	if r.status_code==200:
		doc=r.json()
		listaimagenes=[]
		for i in doc["cards"]:
			listaimagenes.append(i["imageUrlHiRes"])
		return render_template("filtro.html",listaimagenes=listaimagenes)
	else:
		abort(404)

@app.route('/clash',methods=['GET'])
def clash():
	return render_template('clash.html')


@app.route('/clash/jugador',methods=['GET','POST'])
def tag():
	h={"Accept":"application/json","authorization":"Bearer %s"%key}
	datos=request.form.get("Nombre")
	datos2=datos.replace("#","%")
	r=requests.get(URL_BASE2+"players/"+datos2,headers=h)
	if r.status_code==200:
		doc=r.json()
		diccarta={}
		listamazo=[]
		for i in doc["currentDeck"]:
			diccarta['imagen']=i["iconUrls"]["medium"]
			diccarta['nombre']=i["name"]
			listamazo.append(diccarta.copy())
		return render_template("tag.html",doc=doc,listamazo=listamazo)
	else:
		abort(404)

@app.route('/clash/clan',methods=['GET','POST'])
def clan():
	h={"Accept":"application/json","authorization":"Bearer %s"%key}
	datos=request.form.get("Clan")
	payload={"name": datos}
	r=requests.get(URL_BASE2+"clans",headers=h,params=payload)
	if r.status_code==200:
		doc=r.json()
		listaclanes=[]
		for i in doc["items"]:
			if i["members"] > 30:
				listaclanes.append(i)
		return render_template("clan.html",listaclanes=listaclanes)
	else:
		abort(404)

@app.route('/clash/ranking',methods=['GET','POST'])
def rank():
	h={"Accept":"application/json","authorization":"Bearer %s"%key}
	datos=request.form.get("Ranking")
	r=requests.get(URL_BASE2+"locations",headers=h)
	if r.status_code==200:
		doc=r.json()
		for i in doc["items"]:
			if i["name"]==datos:
				idloc=i["id"]
				idloc=str(idloc)
				payload={"limit": 25}
				r2=requests.get(URL_BASE2+"locations/"+idloc+"/rankings/players",headers=h,params=payload)
				if r2.status_code==200:
					doc2=r2.json()
					return render_template("rank.html",doc2=doc2,pais=datos)
					break
				else:
					abort(404)
	else:
		abort(404)	
if __name__ == '__main__':
	app.run('0.0.0.0',8000)
