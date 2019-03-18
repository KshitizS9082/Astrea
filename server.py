from flask import Flask,request
from elasticsearch_dsl import Search,Q
from elasticsearch import Elasticsearch
import json


ES_HOST   = {"host":"localhost","port":9200}
client = Elasticsearch(hosts=[ES_HOST])


app = Flask(__name__)

@app.route("/")
def welcome():
    return ("Server Started")

@app.route("/search")
def search():
    query=request.args.get('q')
    s = Search(using=client)
    q1=Q('multi_match',query=query,fuzziness="1")
    should =[]
    should.append(q1)
    judge = request.args.get('judge')
    if(judge is not None):
        q2 = Q('multi_match',query=judge,fields=['Judge'])
        should.append(q2)
    q = Q('bool',should=should,minimum_should_match=len(should))
    s=s.query(q)
    count=s.count()
    response = s[0:count].execute()
    response= response.to_dict()
    result={}
    for i in range(len(response['hits']['hits'])):
        resp = response['hits']['hits'][i]["_source"]
        resp['score']=response['hits']['hits'][i]["_score"]
        result[str(i)]=resp
    return json.dumps(result)