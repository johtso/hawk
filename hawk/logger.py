#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime


class Logger(object):
    """Task result logger"""
    def __init__(self, mongo_db):
        self.db = mongo_db

    def log_result(self, result):
        task = result.task
        if result.error:
            self._add_alert(task, 'Error: %s' % (result.error, ))
            self._flag_task(task.id)
        elif result.outcome == True:
            self._add_alert(task, 'Triggered')
            self._flag_task(task.id)
    
    def _add_alert(self, task, result):
        self.db.log.insert({'date': datetime.utcnow(),
                            'task_id': task.id,
                            'task': task.title,
                            'result': result})

    def _flag_task(self, task_id):
        self.db.flags.insert({
             'task_id': task_id,
             'triggered': True
            })