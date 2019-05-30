from flask import Flask, render_template, request, abort
import requests
app = Flask(__name__)
@app.route('/',methods=['GET'])
def inicio():
	return render_template("index.html")

@app.route('/pokemontcg',methods=['GET'])
@app.route('/pokemontcg/<id>',methods=['GET'])
def cartas(id=1):
	URL_BASE="https://api.pokemontcg.io/v1/"
	payload={"page": id,"pageSize":30}
	r=requests.get(URL_BASE+"cards",params=payload)
	if r.status_code==200:
		doc=r.json()
		listaimagenes=[]
		for i in doc["cards"]:
			listaimagenes.append(i["imageUrlHiRes"])
		return render_template("pokemon.html",listaimagenes=listaimagenes,id=int(payload["page"]))
	else:
		abort(404)

app.run('0.0.0.0',debug=True)
