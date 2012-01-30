#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import environ
import json
from datetime import datetime

import requests

class Task(object):
    def __init__(self,
        gist_id,
        filename,
        title,
        task_func,
        url=None,
        disabled=False):

        self.gist_id = gist_id
        self.filename = filename
        self.title = title
        self.task_func = task_func
        self.url = url
        self.disabled = disabled

        self.id = gist_id + filename
    
    @classmethod
    def from_taskfile(cls, taskfile):
        gist_id = taskfile.gist_id
        filename = taskfile.filename
        task_string = taskfile.task_string

        lcl = {}
        exec task_string in globals(), lcl
        task = lcl['task']

        return cls(gist_id, filename, **task)
    
    def __repr__(self):
        return '<Task "%s">' % (self.title, )

class TaskFile(object):
    def __init__(self, gist_id, filename, task_string):
        self.gist_id = gist_id
        self.filename = filename
        self.task_string = task_string
        
        self.id = gist_id + filename

class Result(object):
    def __init__(self, task, outcome=False, error=None):
        self.task = task
        self.outcome = outcome
        self.error = error

class Checker(object):
    def __init__(self, gist_id, mongo_db):
        self.db = mongo_db
        self.gist_id = gist_id
        self.task_files = self.fetch_tasks()
        
    def fetch_tasks(self):
        url = 'https://api.github.com/gists/%s' % (self.gist_id, )
        gist = json.loads(requests.get(url).text)

        if gist['public'] == True:
            raise Exception('Please use a private Gist')

        task_files = []
        for gist_file in gist['files'].values():
            task_file =  TaskFile(self.gist_id,
                                  gist_file['filename'],
                                  gist_file['content'])
            task_files.append(task_file)
        
        return task_files

    def run_tasks(self):
        for task_file in self.task_files:

            print 'Running task:', task_file.id

            if self.task_is_flagged(task_file.id):
                print 'Task already flagged, skipping.'
                continue
            try:
                task = Task.from_taskfile(task_file)
            except Exception as e:
                print 'Error parsing task: %s' % (e, )
                continue

            if task.disabled:
                print 'Task disabled, skipping.'
                continue

            try:
                outcome = task.task_func()
            except Exception as e:
                print 'Task threw an exception :('
                yield Result(task, error=e)
            else:
                yield Result(task, outcome)
     
    def task_is_flagged(self, task_id):
        return self.db.flags.find_one({
                  'task_id': task_id,
                  'triggered': True
                 })