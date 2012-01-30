Hawk: Easy Alerts
=====================

Define tasks in a Github Gist, and consume the alerts in the form of an Atom feed.


Environment Variables
---------------------

- ``MONGOLAB_URI`` - URI for your MongoDB database.
- ``FEED_SECRET`` - Secret string that is appended to your feed URL.
- ``GIST_ID`` - ID of the Gist containing your tasks.


Tasks
-----

Here's an example task:

::

    def f():
      import json
      import requests
      resp = json.loads(requests.get('http://johtso.herokuapp.com/cointoss').text)
      return resp['result'] == True

    task = {
        'title': 'Coin toss',
        'task_func': f,
        'disabled': False,
    }