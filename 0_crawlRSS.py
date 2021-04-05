import feedparser
import json

dataFolder = "data/raw/"

RSS_BBC = feedparser.parse("http://feeds.bbci.co.uk/news/rss.xml")
RSS_CNN = feedparser.parse("http://rss.cnn.com/rss/edition.rss")
RSS_NYT = feedparser.parse("https://rss.nytimes.com/services/xml/rss/nyt/World.xml")
RSS_DMail = feedparser.parse("https://www.dailymail.co.uk/news/index.rss")
RSS_TG = feedparser.parse("https://www.theguardian.com/international/rss")
# entry = NewsFeed.entries[1]

def parseAndSaveEntry(entry, baseURL, feedName):
    pure_id = entry.id.replace(baseURL, '') 
    pure_id = pure_id.replace('.html', '') 
    pure_id = pure_id.replace('/', '_') 
    pure_id = pure_id.replace(':', '_') 
    pure_id = pure_id.replace('.', '-')
    pure_id = pure_id.replace('&', '-')
    pure_id = pure_id.replace('=', '-')
    pure_id = pure_id.replace('?', '-')

    News_String = json.dumps(entry)
    f = open(dataFolder +  feedName + "/" + str(pure_id) + ".json", "w")
    f.write(News_String)
    f.close()

for entry in RSS_BBC.entries:
    parseAndSaveEntry(entry, 'https://www.bbc.co.uk/', "rss_bbc")

for entry in RSS_CNN.entries:
    parseAndSaveEntry(entry, 'https://www.cnn.com/', "rss_cnn")

for entry in RSS_NYT.entries:
    parseAndSaveEntry(entry, 'https://www.nytimes.com/', "rss_nyt")

for entry in RSS_DMail.entries:
    parseAndSaveEntry(entry, 'https://www.dailymail.co.uk/', "rss_dmail")

for entry in RSS_TG.entries:
    parseAndSaveEntry(entry, 'https://www.theguardian.com/', "rss_tg")




