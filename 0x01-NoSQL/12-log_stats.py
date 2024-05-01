#!/usr/bin/env python3
"""
First restore backup into database using mongorestore dump
a Python script that provides some stats
about Nginx logs stored in MongoDB:
Database: logs, Collection: nginx
first line: x logs where
x is the number of documents in this collection
second line: Methods:
5 lines with the number of documents with the
method = ["GET", "POST", "PUT", "PATCH", "DELETE"] in this order
one line with the number of documents with:
method=GET
path=/status
You can use this dump as data sample: dump.zip
"""


from pymongo import MongoClient
client = MongoClient(host="localhost", port=27017)
collection = client.logs.nginx
methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
print("{} logs".format(collection.count_documents({})))
print("Methods:")
for method in methods:
    print("\tmethod {}: {}".format(method, collection.count_documents(
        {"method": method})))
print("{} status check".format(collection.count_documents(
    {"method": "GET", "path": "/status"})))
