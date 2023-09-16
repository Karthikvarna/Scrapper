from pymongo import MongoClient

import urllib.parse
from urllib.parse import quote_plus

username = quote_plus('karthikvarna')
password = quote_plus('Orange@12')
client = MongoClient('mongodb+srv://' + username +':' + password + '@cluster0.ts0yzkw.mongodb.net/')

db = client.scrapy

posts = db.test_collection

doc = post = {"author":"Mike",
              "text":"My",
              "tags":["manga","penga"],
              }

post_id = posts.insert_one(post).inserted_id 

print(post_id)

 