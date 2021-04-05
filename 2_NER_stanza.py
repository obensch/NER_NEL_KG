import stanza
import pandas as pd

stanza.download('en')

import time
import json
import numpy as np
import glob, os
from datetime import datetime
import time

nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,ner')

dataPreFolder = "data/preprocessed/"

start = time.time()

def loadFile(name):
    f = open(dataPreFolder + name + ".json", "r")
    news = json.loads(f.read())
    f.close()
    return news

def ner(all_news, entities):
    entity_id = len(entities)
    entity_counter = 0
    for news in all_news:
        news_id = news['news_id']
        doc = nlp(news['text'])
        for sent in doc.sentences:
            for ent in sent.ents:
                entity_counter = entity_counter + 1
                found = False
                for x in entities:
                    if x['text'] == ent.text and x['type'] == ent.type:
                        found = True
                        x['news_ids'].append(news_id)
                        x['amount'] = x['amount'] + 1
                        if 'entities' in news:
                            news['entities'].append(x['id'])
                        else:
                            news['entities'] = [x['id']]
                if not found:
                    entity = {
                        "id": entity_id,
                        "text": ent.text,
                        "type": ent.type,
                        "amount": 1,
                        "news_ids": [news_id]
                    }
                    entities.append(entity)
                    if 'entities' in news:
                        news['entities'].append(entity_id)
                    else:
                        news['entities'] = [entity_id]
                    entity_id = entity_id + 1
    return entities, entity_counter, all_news

def getSortedList(entities):
    ent_text = []
    ent_amount = []
    ent_type = []

    for ent in entities:
        ent_text.append(ent['text'])
        ent_amount.append(ent['amount'])
        ent_type.append(ent['type'])

    d={"text":ent_text, "amount": ent_amount, "type": ent_type}
    df = pd.DataFrame(data=d)
    sorted_list = df.sort_values(by='amount', ascending=False)
    return sorted_list

def writeEntities(entities, entity_counter, news_counter, name):
    f = open(dataStanzaFolder + name + ".json", "w")
    f.write(json.dumps(reddit_entities))
    f.close()

all_entities = []
print("Detecting entities for Reddit")
reddit_news = loadFile("reddit")
all_entities, reddit_entities, n_reddit_news = ner(reddit_news, all_entities)
print("Found ", reddit_entities, " entities in ", len(reddit_news), " news. Total entities detected: " , len(all_entities))

print("Detecting entities for RSS BBC")
rss_bbc = loadFile("rss_bbc")
all_entities, bbc_entities, n_rss_bbc = ner(rss_bbc, all_entities)
print("Found ", bbc_entities, " entities. in ", len(rss_bbc), " news. Total entities detected: " , len(all_entities))

print("Detecting entities for RSS CNN")
rss_cnn = loadFile("rss_cnn")
all_entities, cnn_entities, n_rss_cnn = ner(rss_cnn, all_entities)
print("Found ", cnn_entities, " entities. in ", len(rss_cnn), " news. Total entities detected: " , len(all_entities))

print("Detecting entities for RSS DMail")
rss_dmail = loadFile("rss_dmail")
all_entities, dmail_entities, n_rss_dmail = ner(rss_dmail, all_entities)
print("Found ", dmail_entities, " entities. in ", len(rss_dmail), " news. Total entities detected: " , len(all_entities))

print("Detecting entities for RSS NYT")
rss_nyt = loadFile("rss_nyt")
all_entities, nyt_entities, n_rss_nyt = ner(rss_nyt, all_entities)
print("Found ", nyt_entities, " entities. in ", len(rss_nyt), " news. Total entities detected: " , len(all_entities))

print("Detecting entities for RSS TG")
rss_tg = loadFile("rss_tg")
all_entities, tg_entities, n_rss_tg = ner(rss_tg, all_entities)
print("Found ", tg_entities, " entities. in ", len(rss_tg), " news. Total entities detected: " , len(all_entities))

f = open("data/entities.json", "w")
f.write(json.dumps(all_entities))
f.close()

all_news_with_entities = n_reddit_news + n_rss_bbc + n_rss_cnn + n_rss_dmail + n_rss_nyt + n_rss_tg
stanzaNews = {
    "Stanza": all_news_with_entities
}

f = open("data/news_stanza.json", "w")
f.write(json.dumps(stanzaNews))
f.close()

end = time.time()
print("Time: ", end - start)
# print("Writing:", len(all_news))
# stanzaObject = {
#     "Stanza": all_news
# }
# FinalString = json.dumps(stanzaObject)

# timestr = time.strftime("%Y_%m_%d-%H_%M")
# f = open("data_stanza/" + timestr + ".json", "w")
# f.write(FinalString)
# f.close()


# for news in reddit_news:
#     title = news['title']
#     news['news_id'] = news_id
#     print(news_id)
#     doc = nlp(title)
#     for sent in doc.sentences:
#         for ent in sent.ents:
#             entity_counter = entity_counter + 1
#             found = False
#             for x in entities:
#                 if x['text'] == ent.text and x['type'] == ent.type:
#                     found = True
#                     x['news_ids'].append(news_id)
#                     x['amount'] = x['amount'] + 1
#             if not found:
#                 entity = {
#                     "text": ent.text,
#                     "type": ent.type,
#                     "amount": 1,
#                     "news_ids": [news_id]
#                 }
#                 entities.append(entity)
#     news_id = news_id + 1
#             # # print(f'entity: {ent.text}\ttype: {ent.type}')
#             # if ent.type not in types:
#             #     types.append(ent.type)
#             #     print(ent.type)
#             # if ent.type not in news:
#             #     news[ent.type] = [ent.text]
#             # else:
#             #     news[ent.type].append(ent.text)
#         # for word in sent.words:
#         #     print(f'word: {word.text}\tupos: {word.upos}\txpos: {word.xpos}\tfeats: {word.feats if word.feats else "_"}')
#         # for token in sent.tokens:
#         #     print(token.text, token.ner)
#     # print("\n")

# print(len(entities), entity_counter)



# f = open(dataStanzaFolder + "reddit_entities.json", "w")
# f.write(json.dumps(reddit_entities))
# f.close()
# reddit_sorted_list = getSortedList(reddit_entities)
# reddit_sorted_list.to_csv(dataStanzaFolder + 'reddit_entities.csv')

# f = open(dataStanzaFolder + "rss_bbc_entities.json", "w")
# f.write(json.dumps(bbc_entities))
# f.close()
# bbc_sorted_list = getSortedList(bbc_entities)
# bbc_sorted_list.to_csv(dataStanzaFolder + 'rss_bbc_entities.csv')