import pandas as pd
from datetime import datetime
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json


entityTypes = ['PERSON','NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW']

f = open("data/entities.json", "r")
entities = json.loads(f.read())
f.close()

print(len(entities))
counter = 0
for ent in entities:
    if ent['type'] in entityTypes:
        counter = counter +1

print("named entities:", counter)

f = open("data/entities_wikified_checked.json", "r")
entities = json.loads(f.read())['checked']
f.close()

counter = 0
for ent in entities:
    if 'dbpedia_Resource' in ent:
        if len(ent['dbpedia_Types']) == 0:
            counter = counter +1
print("Entities with DBpedia resource, but no type:", counter)