import sparql
import json
import pandas as pd
import time

start = time.time()

entityTypes = ['PERSON','NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW']
s = sparql.Service("http://dbpedia.org/sparql", "GET")

f = open("data/entities.json", "r")
entities = json.loads(f.read())
f.close()

found_num = 0
for entity in entities:
    # print(row['id'], row['text'], row['type'])
    if entity['type'] in entityTypes:
        searchText = entity['text'].replace('"', '')
        curQuery = 'SELECT DISTINCT * WHERE '
        curQuery = curQuery + '{ ?url rdfs:label "' + searchText + '"@en . '
        curQuery = curQuery + 'FILTER(STRSTARTS(str(?url), "http://dbpedia.org/resource/"))}'
        print(curQuery)
        results = s.query(curQuery).fetchall()
        if len(results) > 0: 
            found_num = found_num + 1
            for result in results:
                resourceName = sparql.unpack_row(result)[0]
                if 'Category:' not in resourceName and 'property' not in resourceName:
                    print(resourceName)
                    entity['dbpedia_Resource'] = resourceName
                    # resourceShort = link.replace('http://dbpedia.org/resource/', '')

print("Found: ",  found_num, "/", len(entities))

f = open("data/entities_wikified.json", "w")
f.write(json.dumps(entities))
f.close()

end = time.time()
print("Time: ", end - start)

# timestr = "2021_04_03-09_07"
# dataStanzaFolder = "data/stanza/"
# dataDBPediaFolder = "data/dbpedia/"
# def dbpediaLookup(df_entities):
#     no_resource = 0
#     df_entities["dbpedia"] = 'None'
#     for index, row in df_entities.iterrows():
#         print(row['id'], row['text'], row['type'])
#         entityType = None
#         if row['type'] in entityTypes:
#             entityType = 'FILTER(STRSTARTS(str(?url), "http://dbpedia.org/resource/"))'
#         if entityType is not None:
#             curQuery = ('SELECT DISTINCT * WHERE { ?url rdfs:label "' + row['text'] + '"@en . FILTER(STRSTARTS(str(?url), "http://dbpedia.org/resource/"))}')
#             results = s.query(curQuery).fetchall()
#             if len(results) == 0: 
#                 no_resource = no_resource + 1
#             else:
#                 for result in results:
#                     link = sparql.unpack_row(result)[0]
#                     if 'Category:' not in link and 'property' not in link:
#                         df_entities.loc[index, "dbpedia"] = link
#                         bestRES = link.replace('http://dbpedia.org/resource/', '')
#     return no_resource, df_entities

# reddit_entities = pd.read_csv(dataStanzaFolder + 'reddit_entities.csv') 
# reddit_no_resource, reddit_new_df = dbpediaLookup(reddit_entities)
# reddit_new_df.to_csv(dataDBPediaFolder + 'reddit_entities.csv')
# print("Reddit: ", reddit_no_resource, len(reddit_entities), len(reddit_new_df))

# rss_bbc_entities = pd.read_csv(dataStanzaFolder + 'rss_bbc_entities.csv') 
# rss_bbc_no_resource, rss_bbc_new_df = dbpediaLookup(rss_bbc_entities)
# rss_bbc_new_df.to_csv(dataDBPediaFolder + 'rss_bbc_entities.csv')
# print("BBC - No resource found for: ", rss_bbc_no_resource, "/", len(rss_bbc_entities), " entities.", len(rss_bbc_new_df))

# rss_cnn_entities = pd.read_csv(dataStanzaFolder + 'rss_cnn_entities.csv') 
# rss_cnn_no_resource, rss_cnn_new_df = dbpediaLookup(rss_cnn_entities)
# rss_cnn_new_df.to_csv(dataDBPediaFolder + 'rss_cnn_entities.csv')
# print("CNN: ", rss_cnn_no_resource, len(rss_cnn_entities), len(rss_cnn_new_df))

# rss_dmail_entities = pd.read_csv(dataStanzaFolder + 'rss_dmail_entities.csv') 
# rss_dmail_no_resource, rss_dmail_new_df = dbpediaLookup(rss_dmail_entities)
# rss_dmail_new_df.to_csv(dataDBPediaFolder + 'rss_dmail_entities.csv')
# print("DailyMail: ", rss_dmail_no_resource, len(rss_dmail_entities), len(rss_dmail_new_df))

# rss_nyt_entities = pd.read_csv(dataStanzaFolder + 'rss_nyt_entities.csv') 
# rss_nyt_no_resource, rss_nyt_new_df = dbpediaLookup(rss_nyt_entities)
# rss_nyt_new_df.to_csv(dataDBPediaFolder + 'rss_nyt_entities.csv')
# print("NYT: ", rss_nyt_no_resource, len(rss_nyt_entities), len(rss_nyt_new_df))

# rss_tg_entities = pd.read_csv(dataStanzaFolder + 'rss_tg_entities.csv') 
# rss_tg_no_resource, rss_tg_new_df = dbpediaLookup(rss_tg_entities)
# rss_tg_new_df.to_csv(dataDBPediaFolder + 'rss_tg_entities.csv')
# print("The Guardian: ", rss_tg_no_resource, len(rss_tg_entities), len(rss_tg_new_df))