from SPARQLWrapper import SPARQLWrapper, JSON
from flask import jsonify


sparql = SPARQLWrapper("http://localhost:3030/watr-dataset/sparql")

def visualise()