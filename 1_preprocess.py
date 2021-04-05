import json
import numpy as np
import glob, os
from datetime import datetime
import codecs

dataRawFolder = "data/raw/"
dataPreFolder = "data/preprocessed/"

def loadFiles(Name):
    all_news = []
    for file in glob.glob(dataRawFolder + Name + "/*.json"):
        f = codecs.open(file, "r", 'utf-8')
        news = json.loads(f.read())
        all_news.append(news)
        f.close()
    return all_news

def saveNews(name, news):
    f = codecs.open(dataPreFolder + name +".json", "w", 'utf-8')
    f.write(json.dumps(news))
    f.close() 

def preProcessReddit(reddits, id_start):
    oldest = 2616977658
    newest = 0
    new_news = []
    for news in all_reddit:
        date = int(float(news['date']))
        news['news_id'] = id_start
        news['reddit_author'] = news['author']
        news['author'] = "reddit"
        news['schema_DateTime'] = datetime.utcfromtimestamp(date).strftime('%Y-%m-%dT%H:%M:%S+00:00')
        news['text'] = news['title']
        news['url'] = news['ex_url']
        new_news.append(news)
        id_start = id_start + 1
        # if date < oldest:
        #     oldest = date
        # if date > newest:
        #    newest = date
    # print("First post:", datetime.utcfromtimestamp(oldest).strftime('%Y-%m-%d %H:%M:%S'), oldest)
    # print("Latest post:", datetime.utcfromtimestamp(newest).strftime('%Y-%m-%d %H:%M:%S'), newest)
    return new_news, id_start

def preProcessRSS(name, feed, id_start):
    new_news = []
    for news in feed:
        if 'published_parsed' in news:
            pub_pars = news['published_parsed']
            news['schema_DateTime'] = "'" + str(pub_pars[0]) + "-" + str(pub_pars[1]).zfill(2) + "-" + str(pub_pars[2]).zfill(2) + "T" 
            news['schema_DateTime'] = news['schema_DateTime'] + str(pub_pars[3]).zfill(2) + ":" + str(pub_pars[4]).zfill(2) + ":" + str(pub_pars[5]).zfill(2) + "+00:00'" 
        else:
            print(news['id'])
        news['news_id'] = id_start
        news['author'] = name
        news['text'] = news['title']
        news['url'] = news['link']
        if 'summary' in news:
            news['text'] = news['text'] + " " + news['summary']
        new_news.append(news)
        id_start = id_start + 1
    return new_news, id_start

cur_id = 0
all_reddit = loadFiles("reddit")
new_reddit, cur_id = preProcessReddit(all_reddit, cur_id)
saveNews("reddit", new_reddit)
print("Reddits preprocessed:", len(all_reddit), " Total:", cur_id)

all_bbc = loadFiles("rss_bbc")
new_bbc, cur_id = preProcessRSS("rss_bbc", all_bbc, cur_id)
saveNews("rss_bbc", new_bbc)
print("BBC preprocessed:", len(all_bbc), " Total:", cur_id)

all_cnn = loadFiles("rss_cnn")
new_cnn, cur_id = preProcessRSS("rss_cnn", all_cnn, cur_id)
saveNews("rss_cnn", new_cnn)
print("CNN preprocessed:", len(all_cnn), " Total:", cur_id)

all_dmail = loadFiles("rss_dmail")
new_dmail, cur_id = preProcessRSS("rss_dmail", all_dmail, cur_id)
saveNews("rss_dmail", new_dmail)
print("DMail preprocessed:", len(all_dmail), " Total:", cur_id)

all_nyt = loadFiles("rss_nyt")
new_nyt, cur_id = preProcessRSS("rss_nyt", all_nyt, cur_id)
saveNews("rss_nyt", new_nyt)
print("NYT preprocessed:", len(all_nyt), " Total:", cur_id)

all_tg = loadFiles("rss_tg")
new_tg, cur_id = preProcessRSS("rss_tg", all_tg, cur_id)
saveNews("rss_tg", new_tg)
print("TG preprocessed:", len(all_tg), " Total:", cur_id)