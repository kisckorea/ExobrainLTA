# -*- coding: utf-8 -*-

'''
dbpedia test code
'''
from SPARQLWrapper import SPARQLWrapper, JSON

type("훈민정음")



sparql = SPARQLWrapper("http://ko.dbpedia.org/sparql")
sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?label
    WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()


sparql.setQuery("""         
            SELECT DISTINCT ?o 
            FROM  <http://ko.dbpedia.org> 
            WHERE { <http://ko.dbpedia.org/resource/훈민정음> <http://dbpedia.org/ontology/abstract> ?o.  FILTER(langMatches(lang(?o), "ko")) }
""")

sparql.setReturnFormat(JSON)
results2 = sparql.query().convert()

sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?label
    WHERE { <http://ko.dbpedia.org/resource/훈민정음> rdfs:label ?label }
""")
sparql.setReturnFormat(JSON)
results3 = sparql.query().convert()

print results2
print results3

result=  results2["results"]["bindings"]
print type(result[0]["o"]["value"])
uni_s= result[0]["o"]["value"]
utf_s=uni_s.encode('utf8')
print type (utf_s)
print utf_s


for result in results["results"]["bindings"]:
#    print(result["label"]["value"])
    pass

for result in results2["results"]["bindings"]:
    s = result["o"]["value"]
    print s
    
for result in results3["results"]["bindings"]:
    #result.decode('cp949')
    s = result["label"]["value"]
    print s
