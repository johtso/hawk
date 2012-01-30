#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import environ
from datetime import datetime
from dateutil.relativedelta import relativedelta

from flask import Flask, request
from pymongo import Connection, uri_parser
from werkzeug.contrib.atom import AtomFeed
import pymongo

from database import database

SECRET = environ['FEED_SECRET']

db = database()

app = Flask(__name__)


@app.route('/%s' % (SECRET, ))
def alert_feed():
    feed = AtomFeed('Recent Events',
                    feed_url=request.url, url=request.url_root)

    yesterday = datetime.utcnow() + relativedelta(days = -1)
    events = db.log.find(limit=10, sort=[('date', pymongo.DESCENDING)])#{'date': {'$gte': yesterday}})

    for event in events:
        feed.add(event['task'], event['result'],
                 content_type='text',
                 id=str(event['_id']),
                 updated=event['date'],
                 published=event['date'])

    return feed.get_response()

if __name__ == '__main__':
    app.debug = True
    app.run()