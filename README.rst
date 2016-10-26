Simple API
=====================

A simple API for managing research studies and submissions. This is for
learning purposes only and has no real-world use.

Installation
------------

::

    pip install -r development.txt

Running the service
-------------------

The recommended way is using Docker:

.. code-block:: bash

    $ inv docker.build
    $ docker-compose -f docker/docker-compose.yml up -d

This will start a server that is accessible at http://127.0.0.1:5000/

Usage
----------

List all studies:

.. code-block:: bash

    $ curl http://127.0.0.1:5000/studies
    {
        "data": []
    }

Create a new study:

.. code-block:: bash

    $ cat study.json
    {
        "data": [{
            "name": "Cape or No Cape?",
            "user": "Hulk",
            "available_places": 10
        }]
    }

    $ curl -H "Content-Type: application/json" -X POST -d @study.json \
        http://127.0.0.1:5000/studies
    {
        "data": [{
            "records": 1
        }]
    }

List all studies belonging to a user:

.. code-block:: bash

    $ curl "http://127.0.0.1:5000/studies?user=Hulk"
    {
        "data": [{
            "_id": "5810ff54354f8600145fbed7",
            "available_places": 10,
            "name": "Cape or No Cape?",
            "user": "Hulk"
        }]
    }


Create a new submission:

.. code-block:: bash

    $ cat submission1.json
    {
        "data": {
            "user": "Iron-Man"
        }
    }

    $ curl -H "Content-Type: application/json" -X POST -d @submission1.json \
        http://127.0.0.1:5000/submission/5810ff54354f8600145fbed7
    {
        "data": [{
            "records": 1
        }]
    }

    $ cat submission2.json
    {
        "data": {
            "user": "Captain America"
        }
    }

    $ curl -H "Content-Type: application/json" -X POST -d @submission2.json \
        http://127.0.0.1:5000/submission/5810ff54354f8600145fbed7
    {
        "data": [{
            "records": 1
        }]
    }

List all submissions within a study:

.. code-block:: bash

    $ curl "http://127.0.0.1:5000/submissions/?study=5810ff54354f8600145fbed7"
    {
        "data": [{
            "_id": "5811017b354f8600145fbedb",
            "created_at": "Wed, 26 Oct 2016 19:18:19 GMT",
            "study": "5810ff54354f8600145fbed7",
            "user": "Iron-Man"
        }, {
            "_id": "58110204354f8600145fbedd",
            "created_at": "Wed, 26 Oct 2016 19:20:36 GMT",
            "study": "5810ff54354f8600145fbed7",
            "user": "Captain America"
        }]
    }

List all submissions belonging to a user

.. code-block:: bash

    $ curl "http://127.0.0.1:5000/submissions/?user=Captain+America"
    {
        "data": [{
            "_id": "58110204354f8600145fbedd",
            "created_at": "Wed, 26 Oct 2016 19:20:36 GMT",
            "study": "5810ff54354f8600145fbed7",
            "user": "Captain America"
        }]
    }
