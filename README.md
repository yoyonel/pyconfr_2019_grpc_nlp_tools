# Twitter Analyzer

> Prototype project for 365Talents

[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
[![CircleCI](https://img.shields.io/circleci/build/github/yoyonel/365talents_twitter_analyzer/develop.svg?token=885581712496df0fba04b76a04b1f6284cba5fb4)](https://circleci.com/gh/yoyonel/365talents_twitter_analyzer/tree/develop)
[![Actions Status](https://github.com/yoyonel/365talents_twitter_analyzer/workflows/Python%20package/badge.svg)](https://github.com/yoyonel/365talents_twitter_analyzer/actions)
<!-- [![Build Status](https://travis-ci.com/yoyonel/forcity_trasherbot.svg?branch=master)](https://travis-ci.com/yoyonel/forcity_trasherbot) -->

Tu développeras un programme Python qui permet de répondre à ces trois questions :
- qui sont les utilisateurs les plus présents sur une timeline Twitter ?
- quel est le sentiment général des tweets (positif ou négatif) d’un utilisateur ?
- à partir du texte d’un tweet, est-il possible de deviner la langue dans lequel le 
tweet a été rédigé ?
 
Tu peux te connecter à l'API Twitter, 
ou utiliser ce petit fichier que tu peux utiliser comme base de tests : [http://bit.ly/365t-data-tweets](http://bit.ly/365t-data-tweets)


## Instructions

Structure is based on [this article](https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure). Source code can be found in the `src` folder, and tests in the `tests` folder.

### Installation

To install the package (development mode):

```bash
➤ pip install -e ".[develop]"
```
(can be long, because of gRPC installation/building)

Need to 'build' the proto(buf) files and generate codes/modules (serializer/parser/...):
```bash
➤ python setup.py build_proto_modules
running build_proto_modules
➤ tree src/tcsctalents/protos 
src/tcsctalents/protos
├── __init__.py
├── StorageService_pb2_grpc.py
├── StorageService_pb2.py
├── StorageService.proto
├── TweetFeaturesService_pb2_grpc.py
├── TweetFeaturesService_pb2.py
├── TweetFeaturesService.proto
├── Tweet_pb2_grpc.py
├── Tweet_pb2.py
└── Tweet.proto
```

We use `en_core_web_sm` spaCy matching model.
We have to download and install this model on our spaCy installation: 
```bash
➤ python -m spacy download en_core_web_sm
Collecting en_core_web_sm==2.1.0 from https://github
.com/explosion/spacy-models/releases/download/en_core_web_sm-2.1.0/en_core_web_sm-2.1.0.tar.gz#egg=en_core_web_sm==2.1.0
  Downloading https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.1.0/en_core_web_sm-2.1.0.tar.gz (11.1MB)
[...]
✔ Download and installation successful
You can now load the model via spacy.load('en_core_web_sm')
```

### Tests

~~We use `tox` for the tests. This ensure a clear separation between the development environment and the test environment.
To launch the tests, run the `tox` command:~~

~~It first starts with a bunch of checks (`flask8` and others) and then launch the tests using python 3.~~

You can use `pytest` for the tests:
```bash
➤ pytest
```

### Running

#### Tools: Cleaning datas -> Tweets JSON File

There is an entrypoint for running a tool `clean_json_tweets`:
```bash
➤ clean_json_tweets -h
usage: clean_json_tweets [-h] [--key_for_indexing KEY_FOR_INDEXING] [-v]
                         [-ll {debug,warning,info,error,critical}]
                         tweet_json output_tweet_json

positional arguments:
  tweet_json            Path to tweets JSON file.
  output_tweet_json     Path to output clean tweets JSON file.

optional arguments:
  -h, --help            show this help message and exit
  --key_for_indexing KEY_FOR_INDEXING
                        Key used/test for indexing tweets. (default=id).
  -v, --verbose         increase output verbosity (enable 'DEBUG' level log)
  -ll {debug,warning,info,error,critical}, --log_level {debug,warning,info,error,critical}
                        The logger filter level. (default=debug).
```

example of utilization:
```bash
➤ clean_json_tweets tests/data/tweets.json tests/data/tweets.clean.json --key_for_indexing id
2019-06-21 11:26:34 - twitter_analyzer.clean_json_tweets - INFO - application version: 0.1.2.dev13+g5790b10.d20190621
2019-06-21 11:26:34 - twitter_analyzer.clean_json_tweets - INFO - Number of rows: 586
2019-06-21 11:26:34 - twitter_analyzer.clean_json_tweets - WARNING - Rows with indexing errors:
                     id                                               text
196  776523223261405184  Ahhh, rich people problems :-) https://t.co/uN...
197  776523223261405184  Ahhh, rich people problems :-) https://t.co/uN...
391  776414205700218881  RT @A_Richardin: Comment les startups à succès...
392  776414205700218881  RT @A_Richardin: Comment les startups à succès...
2019-06-21 11:26:34 - twitter_analyzer.clean_json_tweets - INFO - After indexing/cleaning, the number rows remaining: 584
2019-06-21 11:26:34 - twitter_analyzer.clean_json_tweets - INFO - Export tweets json to: `tests/data/tweets.clean.json`
```

#### In-Memory

Simple (naive) version with tweets in-memory dump (for each invocation).

For each command/processing features to perform, we have to provide a tweets json dump.

Example for `top users`:
```bash
➤ twitter_analyzer_in_memory --tweet_json tests/data/tweets.json top_user -ts 2016 -te 2017
2019-06-17 15:37:07 - tcsctalents.twitter_analyzer.clients.client_in_memory - DEBUG - Load all tweets in memory ...      
2019-06-17 15:37:07 - tcsctalents.twitter_analyzer.models.Tweet - ERROR - lang='in' not in lang list     
2019-06-17 15:37:07 - tcsctalents.twitter_analyzer.models.Tweet - ERROR - lang='in' not in lang list     
2019-06-17 15:37:07 - tcsctalents.twitter_analyzer.models.Tweet - ERROR - lang='in' not in lang list     
2019-06-17 15:37:07 - tcsctalents.twitter_analyzer.clients.client_in_memory - DEBUG - Build Time series ...      
2019-06-17 15:37:07 - tcsctalents.twitter_analyzer.clients.client_in_memory - INFO - Processing Top Users feature ...
2019-06-17 15:37:07 - tcsctalents.twitter_analyzer.clients.client_in_memory - INFO - TopUser user_id=11322372 nb_tweets=1
2019-06-17 15:37:07 - tcsctalents.twitter_analyzer.clients.client_in_memory - INFO - TopUser user_id=13334762 nb_tweets=1
2019-06-17 15:37:07 - tcsctalents.twitter_analyzer.clients.client_in_memory - INFO - TopUser user_id=15234407 nb_tweets=1
[...]
2019-06-17 15:37:07 - tcsctalents.twitter_analyzer.clients.client_in_memory - INFO - TopUser user_id=1269648812 nb_tweets=25
2019-06-17 15:37:07 - tcsctalents.twitter_analyzer.clients.client_in_memory - INFO - TopUser user_id=1236101 nb_tweets=39
2019-06-17 15:37:07 - tcsctalents.twitter_analyzer.clients.client_in_memory - INFO - TopUser user_id=592843104 nb_tweets=41
```

Example for `general sentiment`:
```bash
➤ twitter_analyzer_in_memory --tweet_json tests/data/tweets.json general_sentiment --user_id 592843104
2019-06-17 15:39:34 - tcsctalents.twitter_analyzer.clients.client_in_memory - DEBUG - Load all tweets in memory ...
2019-06-17 15:39:34 - tcsctalents.twitter_analyzer.models.Tweet - ERROR - lang='in' not in lang list
2019-06-17 15:39:34 - tcsctalents.twitter_analyzer.models.Tweet - ERROR - lang='in' not in lang list
2019-06-17 15:39:34 - tcsctalents.twitter_analyzer.models.Tweet - ERROR - lang='in' not in lang list
2019-06-17 15:39:34 - tcsctalents.twitter_analyzer.clients.client_in_memory - DEBUG - Build Time series ...
2019-06-17 15:39:34 - tcsctalents.twitter_analyzer.clients.client_in_memory - DEBUG - General sentiment computed from user_id=592843104 tweets: GeneralSentiment sentiment=<Sentiment polarity=0.17984959349593493 subjectivity=0.20130081300813002> timeline=<Timeline start=Timestamp('2016-09-15 05:54:38+0000', tz='tzutc()') end=Timesta… nb_tweets=41
2019-06-17 15:39:34 - tcsctalents.twitter_analyzer.clients.client_in_memory - INFO - General tweets sentiment from user_id=592843104 => positive
```

Example for `detect language`:
```bash
➤ twitter_analyzer_in_memory --tweet_json tests/data/tweets.json detect_language --tweet_id 776655406764613632
2019-06-17 15:40:35 - tcsctalents.twitter_analyzer.clients.client_in_memory - DEBUG - Load all tweets in memory ...
2019-06-17 15:40:35 - tcsctalents.twitter_analyzer.models.Tweet - ERROR - lang='in' not in lang list
2019-06-17 15:40:35 - tcsctalents.twitter_analyzer.models.Tweet - ERROR - lang='in' not in lang list
2019-06-17 15:40:35 - tcsctalents.twitter_analyzer.models.Tweet - ERROR - lang='in' not in lang list
2019-06-17 15:40:35 - tcsctalents.twitter_analyzer.clients.client_in_memory - DEBUG - Build Time series ...
2019-06-17 15:40:35 - tcsctalents.twitter_analyzer.clients.client_in_memory - DEBUG - Detect language on tweet (id=776655406764613632): DetectLanguage language='pt' score=0.5714289547534985
2019-06-17 15:40:35 - tcsctalents.twitter_analyzer.clients.client_in_memory - INFO - (id=776655406764613632, text="Cinéma (porno) de plein air 🙃 https://t.co/I6qGD4LwrL") -> Portugues
```
(ps: bug exposed here with the method for detecting language ! :p)

#### RPC

##### MongoDB
First, we need to launch a MongoDB server (local or with docker container):
```bash
➤ make up  
docker-compose -f docker/docker-compose.yml up
Starting docker_mongodb_1 ... done
Attaching to docker_mongodb_1
[...]
```

Test if the docker container running and port/connection establishment:
```bash
➤ docker ps 
CONTAINER IDIMAGE     COMMAND  CREATED     STATUS      PORTS      NAMES
8d47ac4f7fb6centos/mongodb-32-centos7      "container-entrypoin…"   6 hours ago Up About a minute   0.0.0.0:27017->27017/tcp   docker_mongodb_1
[...]
➤ sudo netstat -tupln | grep 27017 
tcp6       0      0 :::27017:::*    LISTEN      31155/docker-proxy  
```

We can check the connection to MongoDB with mongo-tools `mongo`:
```bash
➤ mongo 127.0.0.1:27017/twitter_analyzer -u user -p password --eval "db.tweets.count()"
connecting to: mongodb://127.0.0.1:27017/twitter_analyzer?gssapiServiceName=mongodb
0
```

##### Storage

For launching the `storage` server:
```bash
➤ make twitter_analyzer_rpc_storage_server 
2019-06-17 15:08:51,066 - tcsctalents.twitter_analyzer.tools.rpc_server - INFO - Starting storage server on [::]:50052...
2019-06-17 15:08:51,069 - tcsctalents.twitter_analyzer.tools.rpc_server - INFO - Ready and waiting for connections.
```

`storage` server provide services for storing tweet (message) into database.
Here an example of client application for dumping json tweets through this rpc/server:
```bash
➤ twitter_analyzer_rpc_storage_dump_json_tweets_into_db -p tests/data/tweets.json
2019-06-17 15:13:15 - tcsctalents.twitter_analyzer.tools.rpc_init_stub - INFO - Connection to: [localhost:50052]/twitter analyzer storage - WAITING ...
2019-06-17 15:13:15 - tcsctalents.twitter_analyzer.tools.rpc_init_stub - INFO - Connection to: [localhost:50052]/twitter analyzer storage - ESTABLISHED
```

and then:
```bash
➤ mongo 127.0.0.1:27017/twitter_analyzer -u user -p password --eval "db.tweets.count()"
connecting to: mongodb://127.0.0.1:27017/twitter_analyzer?gssapiServiceName=mongodb
582
➤ mongo 127.0.0.1:27017/twitter_analyzer -u user -p password --eval "db.tweets.find()"
{ "_id" : ObjectId("5d0793574d2fcbd8e1dc3404"), "created_at" : ISODate("2016-09-16T09:14:47Z"), "user_id" : "183749519", "text" : "The only thing worse than a political insider is the sort of candidate you get when people use their vote to protest against insiders.", "lang" : "en", "tweet_id" : "776710916700340224" }
{ "_id" : ObjectId("5d0793574d2fcbd8e1dc3405"), "created_at" : ISODate("2016-09-16T09:12:31Z"), "user_id" : "592843104", "text" : "RT @Marion_Demos: Les nouvelles utopies managériales https://t.co/NJtn5ISY5l via @HubertLandier https://t.co/9kX6sQKwzi RT @Geuze_F", "lang": "fr", "tweet_id" : "776710345499021312" }
```

##### Features processing

Once the database loaded (with datas), 
we can launch a `tweet features` server:
```bash
➤ make twitter_analyzer_rpc_features_server
2019-06-17 15:24:32,013 - tcsctalents.twitter_analyzer.tools.rpc_server - INFO - Starting features processing server on [::]:50051...
2019-06-17 15:24:32,014 - tcsctalents.twitter_analyzer.tools.rpc_server - INFO - Ready and waiting for connections.
```

`tweet features` provide services for launching processing on tweets:
- listing `top users` for a specific timeline
- compute the `general sentiment` of tweets emit by a twitter users
- `detect language` from text of a specific tweet

Example for `top users`:
```bash
➤ twitter_analyzer_rpc_features_client top_user -ts 2016 -te 2017 
2019-06-17 15:27:59 - tcsctalents.twitter_analyzer.tools.rpc_init_stub - INFO - Connection to: [localhost:50051]/twitter analyzer features processor - WAITING ...       
2019-06-17 15:27:59 - tcsctalents.twitter_analyzer.tools.rpc_init_stub - INFO - Connection to: [localhost:50051]/twitter analyzer features processor - ESTABLISHED       
2019-06-17 15:27:59 - tcsctalents.twitter_analyzer.clients.client_rpc_features_processing - INFO - #1 - user_id=592843104, nb_tweets=41     
2019-06-17 15:27:59 - tcsctalents.twitter_analyzer.clients.client_rpc_features_processing - INFO - #2 - user_id=1236101, nb_tweets=39       
2019-06-17 15:27:59 - tcsctalents.twitter_analyzer.clients.client_rpc_features_processing - INFO - #3 - user_id=15808647, nb_tweets=25
[...]
2019-06-17 15:27:59 - tcsctalents.twitter_analyzer.clients.client_rpc_features_processing - INFO - #107 - user_id=70596949, nb_tweets=1
2019-06-17 15:27:59 - tcsctalents.twitter_analyzer.clients.client_rpc_features_processing - INFO - #108 - user_id=776688817285857280, nb_tweets=1
2019-06-17 15:27:59 - tcsctalents.twitter_analyzer.clients.client_rpc_features_processing - INFO - #109 - user_id=891360379, nb_tweets=1
```

Example for `general sentiment`:
```bash
➤ twitter_analyzer_rpc_features_client general_sentiment --user_id 592843104
2019-06-17 15:29:27 - tcsctalents.twitter_analyzer.tools.rpc_init_stub - INFO - Connection to: [localhost:50051]/twitter analyzer features processor - WAITING ...
2019-06-17 15:29:27 - tcsctalents.twitter_analyzer.tools.rpc_init_stub - INFO - Connection to: [localhost:50051]/twitter analyzer features processor - ESTABLISHED
2019-06-17 15:29:27 - tcsctalents.twitter_analyzer.clients.client_rpc_features_processing - DEBUG - {'sentiment': {'polarity': 0.17984959483146667, 'subjectivity': 0.20130081474781036}, 'timeline': {'start': '1473918878000', 'end': '1474017151000'}, 'nbTweets': '41'}
2019-06-17 15:29:27 - tcsctalents.twitter_analyzer.clients.client_rpc_features_processing - INFO - General tweets sentiment from user_id=592843104 => positive
```

Example for `detect language`:
```bash
➤ twitter_analyzer_rpc_features_client detect_language --tweet_id 776655406764613632
2019-06-17 15:30:28 - tcsctalents.twitter_analyzer.tools.rpc_init_stub - INFO - Connection to: [localhost:50051]/twitter analyzer features processor - WAITING ...
2019-06-17 15:30:28 - tcsctalents.twitter_analyzer.tools.rpc_init_stub - INFO - Connection to: [localhost:50051]/twitter analyzer features processor - ESTABLISHED
2019-06-17 15:30:29 - tcsctalents.twitter_analyzer.clients.client_rpc_features_processing - DEBUG - Detect language on tweet (id=776655406764613632): {'language': 'pt', 'score': 0.857140302658081}
2019-06-17 15:30:29 - tcsctalents.twitter_analyzer.clients.client_rpc_features_processing - INFO - id=776655406764613632 -> Portuguese
```
