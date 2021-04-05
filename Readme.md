# Named Entity Recognition and Named Entity Linking with Stanza to create a Knowledge Graph out of RSS News and Subreddits

"data" folder:
Contains all the data of the project.

"data/raw" folder:
Contains all crawled news from reddit and rss from 22.03.2021 till 05.04.2021.
Data crawled with the 0_crawlReddit.py and 0_crawlRSS.py scripts.

"data/prepprocessed" folder:
Contains all the preprocessed news created by the 1_preprocess.py script.
Files created by 1_preprocess.py.

"data/news_stanza.json"
Contains all news processed by stanza with ids of connected entities.
File created by 2_NER_stanza.py

"data/entities.json"
Contains all entities detected by stanza including connected news_ids.
File created by 2_NER_stanza.py

"data/entities_wikified.json"
Contains all entities including dbpedia resources if available.
File created by 3_SPARQL_Wikify.py

"data/entities_wikified_checked.json"
Contains all entities including dbpedia resources and boolean if stanza type matches the dbpedia ontology of resource.
File created by 4_SPARQL_Check.py

0_crawlReddit.py:
Crawls the subreddit "news" using the python library praw and stores new posts into the "data/raw/reddit" folder.

0_crawlRSS.py:
Crawls the declared rss feeds using the python library feedparser and stores new feeds into the "data/raw/FEED_NAME" folder

1_preprocess.py:
Preprocesses all reddit and rss data to align field names and datetimes, and creates an index for all news.

2_NER_stanza.py:
Runs stanza named entity recognition pipeline on the preprocessed news and stores detected entities into "data/entities.json" and news into "data/news_stanza.json".

3_SPARQL_Wikify.py:
Runs a SPARQL query against the dbpedia SPARQL endpoint to check if an resource exists for each entity.

4_SPARQL_Check.py:
Runs a SPARQL query against the dbpedia SPARQL endpoint to check if the detected stanza class matches the resource ontology.

5_News.yarrr.yml / rules.rml.ttl / graph.ttl:
Use following command to generate rml mapping out of mapping file:
yarrrml-parser -i .\5_News.yarrr.yml -o rules.rml.ttl
In a next step the following command is used to generate turtle tripples:
java -jar .\rmlmapper.jar -m .\rules.rml.ttl -o graph.ttl

6_CountEntities.py:
Python script to count the named entities and dbpedia resources without a type.

requirements.txt:
All used python libraries.

SPARQL_Queries.txt:
Used queries and results.
