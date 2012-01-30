#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import environ

from pymongo import Connection, uri_parser

def database():
    mongodb_uri = uri_parser.parse_uri(environ['MONGOLAB_URI'])

    conn = Connection(*mongodb_uri['nodelist'][0])
    db = conn[mongodb_uri['database']]
    db.authenticate(mongodb_uri['username'], mongodb_uri['password'])

    return db