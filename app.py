from flask import Flask, render_template, request, abort
import requests
import os
import json
app = Flask(__name__)
URL_BASE="https://api.pokemontcg.io/v1/"
URL_BASE2="https://api.clashroyale.com/v1/"
key=os.environ["keyclash"]


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
		return render_template("tag.html",doc=doc)
	else:
		abort(404)

app.run('0.0.0.0',debug=True)
