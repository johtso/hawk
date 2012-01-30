#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import environ

from flaskext.script import Manager

from hawk import app
from hawk.database import database
from hawk.checker import Checker
from hawk.logger import Logger

GIST_ID = environ['GIST_ID']

manager = Manager(app)

db = database()

@manager.command
def clear(thing):
    """Clear the database."""
    if thing in ('flags', 'all'):
        db.flags.remove({})
        print 'All flags cleared.'
    if thing in ('alerts', 'all'):
        db.log.remove({})
        print 'All alerts cleared.'

@manager.command
def show(thing):
    if thing in ('flags', 'all'):
        for flag in db.flags.find():
            print flag
    if thing in ('alerts', 'all'):
        for alert in db.log.find():
            print alert

@manager.command
def testtasks():
    """Run all tasks and print results"""
        
    checker = Checker(GIST_ID, db)
    for result in checker.run_tasks():
        print result.__dict__

@manager.command
def runtasks():
    """Run all tasks and add results to log"""
    
    checker = Checker(GIST_ID, db)
    logger = Logger(db)

    for result in checker.run_tasks():
        print result.__dict__
        logger.log_result(result)

if __name__ == "__main__":
    manager.run()