import sparql
import json
import pandas as pd

s = sparql.Service("http://dbpedia.org/sparql", "GET")

PERSON_DBpedia_Ontologies = ["person"]
NORP_DBpedia_Ontologies = ["political party"]
FACILITY_DBpedia_Ontologies = ["place"]
ORG_DBpedia_Ontologies = ["company", "organisation"]
GPE_DBpedia_Ontologies = ["city", "country", "region", "settlement"]
LOC_DBpedia_Ontologies = ["place"]
PRODUCT_DBpedia_Ontologies = ["product"]
EVENT_DBpedia_Ontologies = ["event"]
WORK_OF_ART_DBpedia_Ontologies = ["work"]
LAW_DBpedia_Ontologies = ["legalForm"]
LANGUAGE_DBpedia_Ontologies = ["language"]

f = open("data/entities_wikified.json", "r")
entities = json.loads(f.read())
f.close()

type_correct_num = 0
for entity in entities:
    if 'dbpedia_Resource' in entity:
        entityType = entity['type']
        curQuery = 'SELECT DISTINCT ?label WHERE {'
        curQuery = curQuery + '<' + entity['dbpedia_Resource'] + '> a ?type . '
        curQuery = curQuery + ' ?type rdfs:label ?label . FILTER (lang(?label) = "en") }'
        results = s.query(curQuery).fetchall()
        labels = []
        for result in results:
            label = sparql.unpack_row(result)[0]
            labels.append(label)
        entity["dbpedia_Types"] = labels

        ontology_match = False
        if entityType == "PERSON":
            ontology_match = any(item in PERSON_DBpedia_Ontologies for item in labels)
        if entityType == "NORP":
            ontology_match = any(item in NORP_DBpedia_Ontologies for item in labels)
        if entityType == "FAC":
            ontology_match = any(item in FACILITY_DBpedia_Ontologies for item in labels)
        if entityType == "ORG":
            ontology_match = any(item in ORG_DBpedia_Ontologies for item in labels)
        if entityType == "GPE":
            ontology_match = any(item in GPE_DBpedia_Ontologies for item in labels)
        if entityType == "LOC":
            ontology_match = any(item in LOC_DBpedia_Ontologies for item in labels)
        if entityType == "PRODUCT":
            ontology_match = any(item in PRODUCT_DBpedia_Ontologies for item in labels)
        if entityType == "EVENT":
            ontology_match = any(item in EVENT_DBpedia_Ontologies for item in labels)
        if entityType == "WORK_OF_ART":
            ontology_match = any(item in WORK_OF_ART_DBpedia_Ontologies for item in labels)
        if entityType == "LAW":
            ontology_match = any(item in LAW_DBpedia_Ontologies for item in labels)
        if entityType == "LANGUAGE":
            ontology_match = any(item in LANGUAGE_DBpedia_Ontologies for item in labels)

        if not ontology_match and len(labels)>0:
            print(entityType, entity['text'], labels)
        
        entity["dbpedia_TypeMatch"] = ontology_match
        if ontology_match:
            type_correct_num = type_correct_num + 1

print("Types correct: ", type_correct_num, "/", len(entities))
checked = {
    "checked": entities
}
f = open("data/entities_wikified_checked.json", "w")
f.write(json.dumps(checked))
f.close()

# def dbpediaCheckTypes(df_entities):
#     no_match = 0
#     df_entities["typesDBpedia"] = 'None'
#     df_entities["typeMatch"] = 'None'
#     for index, row in df_entities.iterrows():
#         if row['dbpedia'] is not None:
#             dbpediaUrl = row['dbpedia']
#             entityType = row['type']
#             curQuery = ('SELECT DISTINCT ?label WHERE { <' + dbpediaUrl + '> a ?type . ?type rdfs:label ?label . FILTER (lang(?label) = "en") }')
#             results = s.query(curQuery).fetchall()
#             labels = []
#             for result in results:
#                 label = sparql.unpack_row(result)[0]
#                 labels.append(label)
#             df_entities.at[index, "typesDBpedia"] = labels

#             ontology_match = False
#             if entityType == "GPE":
#                 for ontology in GPE_DBpedia_Ontologies:
#                     if ontology in labels:
#                         ontology_match = True
#             if entityType == "PERSON":
#                 for ontology in PERSON_DBpedia_Ontologies:
#                     if ontology in labels:
#                         ontology_match = True
#             if entityType == "ORG":
#                 for ontology in ORG_DBpedia_Ontologies:
#                     if ontology in labels:
#                         ontology_match = True

#             if entityType == "FAC":
#                 for ontology in FACILITY_DBpedia_Ontologies:
#                     if ontology in labels:
#                         ontology_match = True

#             if entityType == "PRODUCT":
#                 for ontology in PRODUCT_DBpedia_Ontologies:
#                     if ontology in labels:
#                         ontology_match = True
            
#             if entityType == "LOC":
#                 for ontology in LOC_DBpedia_Ontologies:
#                     if ontology in labels:
#                         ontology_match = True

#             if entityType == "EVENT":
#                 for ontology in EVENT_DBpedia_Ontologies:
#                     if ontology in labels:
#                         ontology_match = True

#             if entityType == "LOCATION":
#                 for ontology in LANGUAGE_DBpedia_Ontologies:
#                     if ontology in labels:
#                         ontology_match = True
                        
#             if not ontology_match and len(labels)>0:
#                 print(entityType, row['text'], labels)
            
#             df_entities.at[index, "typeMatch"] = ontology_match
#     return no_match, df_entities

# reddit_entities = pd.read_csv(dataDBPediaFolder + 'reddit_entities.csv') 
# reddit_no_resource, reddit_new_df = dbpediaCheckTypes(reddit_entities)
# reddit_new_df.to_csv(dataDBPediaFolder + 'reddit_entities.csv')
# print("Reddit: ", reddit_no_resource, len(reddit_entities), len(reddit_new_df))

# rss_bbc_entities = pd.read_csv(dataDBPediaFolder + 'rss_bbc_entities.csv') 
# rss_bbc_no_resource, rss_bbc_new_df = dbpediaCheckTypes(rss_bbc_entities)
# rss_bbc_new_df.to_csv(dataDBPediaFolder + 'rss_bbc_entities.csv')
# print("BBC: ", rss_bbc_no_resource, len(rss_bbc_entities), len(rss_bbc_new_df))

# rss_cnn_entities = pd.read_csv(dataDBPediaFolder + 'rss_cnn_entities.csv') 
# rss_cnn_no_resource, rss_cnn_new_df = dbpediaCheckTypes(rss_cnn_entities)
# rss_cnn_new_df.to_csv(dataDBPediaFolder + 'rss_cnn_entities.csv')
# print("CNN: ", rss_cnn_no_resource, len(rss_cnn_entities), len(rss_cnn_new_df))

# rss_dmail_entities = pd.read_csv(dataDBPediaFolder + 'rss_dmail_entities.csv') 
# rss_dmail_no_resource, rss_dmail_new_df = dbpediaCheckTypes(rss_dmail_entities)
# rss_dmail_new_df.to_csv(dataDBPediaFolder + 'rss_dmail_entities.csv')
# print("DailyMail: ", rss_dmail_no_resource, len(rss_dmail_entities), len(rss_dmail_new_df))

# rss_nyt_entities = pd.read_csv(dataDBPediaFolder + 'rss_nyt_entities.csv') 
# rss_nyt_no_resource, rss_nyt_new_df = dbpediaCheckTypes(rss_nyt_entities)
# rss_nyt_new_df.to_csv(dataDBPediaFolder + 'rss_nyt_entities.csv')
# print("NYT: ", rss_nyt_no_resource, len(rss_nyt_entities), len(rss_nyt_new_df))

# rss_tg_entities = pd.read_csv(dataDBPediaFolder + 'rss_tg_entities.csv') 
# rss_tg_no_resource, rss_tg_new_df = dbpediaCheckTypes(rss_tg_entities)
# rss_tg_new_df.to_csv(dataDBPediaFolder + 'rss_tg_entities.csv')
# print("The Guardian: ", rss_tg_no_resource, len(rss_tg_entities), len(rss_tg_new_df))

# counter_entites = 0
# counter_zeros = 0
# couter_perfect = 0
# couter_loc_match = 0
# couter_loc_not_match = 0

# foundRes = []
# missRes = []

# singleEnts = []

# for i in range(len(news)): # len(news)
#     for entityType in entityTypes:
#         if entityType in news[i]:
#             for entity in news[i][entityType]:
#                 counter_entites = counter_entites + 1
#                 if entity not in singleEnts:
#                     singleEnts.append(entity)
#                 curQuery = ('SELECT DISTINCT * WHERE { ?entity rdfs:label "' + entity + '"@en .}')
#                 results = s.query(curQuery).fetchall()
#                 if len(results) == 0: 
#                     counter_zeros = counter_zeros + 1 
#                     # print("Missing: ", entity, entityType)
#                     missing = {
#                         "Entity": entity,
#                         "Type": entityType
#                     }
#                     missRes.append(missing)
#                 else:
#                     for result in results:
#                         link = sparql.unpack_row(result)[0]
#                         if 'Category:' not in link and 'property' not in link:
#                             bestRES = link.replace('http://dbpedia.org/resource/', '')
#                             couter_perfect = couter_perfect + 1
#                             if entityType == "LOC":
#                                 classQuery = ('ASK WHERE { <http://dbpedia.org/resource/' + bestRES + '> a <http://dbpedia.org/ontology/Location> .}')
#                                 classResult = s.query(classQuery).hasresult()
#                                 if classResult:
#                                     couter_loc_match = couter_loc_match +1
#                                 else: 
#                                     couter_loc_not_match = couter_loc_not_match + 1
#                                 print(classResult, couter_loc_match, couter_loc_not_match)
#                             print(couter_perfect, counter_entites, entityType, entity, bestRES)
#                             match = {
#                                 "Entity": entity,
#                                 "Result": bestRES,
#                                 "Type": entityType
#                             }
#                             foundRes.append(match)
#                     # print(len(results), values)

# # print("Entities: ", counter_entites, " Single: ", len(singleEnts))
# # print("Miss: ", len(missRes), " Match: ", len(foundRes))
# # timestr = time.strftime("%Y_%m_%d-%H_%M")
# # f = open("data_stanza/" + timestr + ".json", "w")
# # f.write(FinalString)
# # f.close() 