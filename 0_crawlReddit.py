import praw
import os
import json
import time

number = 100
sleep_time = 60
id="sHtLL5NaCEJNuw"
secret="_7lRXMZxnSKM1s-afRxPoC2JOnqOZA"
agent = "NER Knowledge Graph Project 0.1"
r = praw.Reddit(client_id=id, client_secret=secret, user_agent=agent)

subreddit = "news"

newsReddit = r.subreddit(subreddit).new(limit=None) # params={"after" : "t3_m2i5wv"}

# con_search = r.subreddit(subreddit).search('timestamp=1616588297..1615438502', subreddit=subreddit, syntax="cloudsearch")

cur_sub = 0
Content = []
for submission in newsReddit:
    print(cur_sub)
    id = submission.id
    title = submission.title
    title_no_quotes = title.replace("'", "")
    ups = submission.ups
    upvote_ratio = submission.upvote_ratio

    date = submission.created_utc
    
    author = submission.author.name
    domain = submission.domain
    ex_url = submission.url
    re_url = "http://reddit.com" + submission.permalink
    # pprint.pprint(vars(submission))
    
    newsEntry = {
        "id": id,
        "title": title_no_quotes,
        "ups": str(ups),
        "upvote_ratio": str(upvote_ratio),
        "date": str(date),
        "author": author,
        "domain": domain,
        "ex_url": ex_url,
        "re_url": re_url
    }
    print(newsEntry)

    News_String = json.dumps(newsEntry)
    f = open("data/raw/reddit/" + str(id) + ".json", "w")
    f.write(News_String)
    f.close()

    cur_sub = cur_sub +1
    Content.append(newsEntry)

timestr = time.strftime("%Y_%m_%d-%H_%M")
FinalString = json.dumps(Content)

f = open("data_json_new/" + timestr + "_" + str(cur_sub) + ".json", "w")
f.write(FinalString)
f.close() 