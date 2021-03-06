=============================
exo_messages
=============================

.. image:: https://badge.fury.io/py/lib-exo-messages.svg
    :target: https://badge.fury.io/py/lib-exo-messages

.. image:: https://travis-ci.org/exolever/lib-exo-messages.svg?branch=master
    :target: https://travis-ci.org/exolever/lib-exo-messages

.. image:: https://codecov.io/gh/exolever/lib-exo-messages/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/exolever/lib-exo-messages

.. image:: https://api.codeclimate.com/v1/badges/d3edc8403472234e7348/test_coverage
    :target: https://codeclimate.com/github/exolever/lib-exo-messages/test_coverage

Library to manage Messages

Documentation
-------------

Quickstart
----------

Install exo_messages::

    pip install lib-exo-messages

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'exo_messages.apps.ExoMessagesConfig',
        ...
    )

Add exo_messages's URL patterns:

.. code-block:: python

    from exo_messages import urls as exo_messages_urls


    urlpatterns = [
        ...
        url(r'^', include(exo_messages_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
