from flask import Flask, render_template, request, abort
import requests
app = Flask(__name__)
URL_BASE="https://api.pokemontcg.io/v1/"

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



app.run('0.0.0.0',debug=True)
