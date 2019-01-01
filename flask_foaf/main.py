from flask import Flask, request, render_template
from rdflib import Graph, Namespace
from flask_table import Table, Col
from rdflib.namespace import FOAF, RDF
from SPARQLWrapper import SPARQLWrapper, JSON


app = Flask(__name__)

# wd = Namespace("http://www.wikidata.org/entity/")
# wdt = Namespace("http://www.wikidata.org/prop/direct/")
# wikibase = Namespace("http://wikiba.se/ontology#")
# bd = Namespace("http://www.bigdata.com/rdf#")

# foaf = Graph()
# foaf.parse("flask_foaf/static/rdf/sparql.rdf")
# foaf.bind('wd', wd)
# foaf.bind('wdt', wdt)
# foaf.bind('wikibase', wikibase)
# foaf.bind('bd', bd)

class ItemTable(Table):
		classes = ["table", "table-hover"]
		wiki = Col('Wiki')
		title = Col('Title')


class Item(object):
		def __init__(self, wiki, title):
			self.wiki = wiki
			self.title = title

def get_table():
 
	wdt = Namespace("https://www.wikidata.org/wiki/Property:")
	rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")

	g = Graph()

	sparql1 = SPARQLWrapper("https://query.wikidata.org/sparql")
	query1 = """
		CONSTRUCT
		{
		  ?item rdfs:label	?itemLabel.
		  ?item wdt:P577	?pubDate
		}
		WHERE 
		{
		  ?item wdt:P31 wd:Q11424.
		  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
		} limit 100
	"""
	sparql1.setQuery(query1)
	sparql1.setReturnFormat(RDF)
	results1 = sparql1.query()
	triples1 = results1.convert()
	g += triples1

	listJudul=[]
	table=""

	for s,p,o in g.triples( (None, rdfs.label, None) ):
		#for x,y,z in g.triples( (s, wdt.P577, None) ):
		#	print (s + " published in " + z)
		print (o)
		sLink = "<a href=" + s + ">"  + o + "</a>"
		listJudul.append(Item(sLink, str(o)))

	table=ItemTable(listJudul)

	if listJudul == []:
		return "No Result"
	else:
		#return listMakanan
		table = table.__html__()
		table = table.replace('&lt;','<')
		table = table.replace('&gt;','>')
	return (table)

	# return listJudul


@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/search", methods=['GET'])
def search_page():
	#search=request.form['search']
	return render_template("search.html", table=get_table())
