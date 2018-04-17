=====
Usage
=====

To use exo_messages in a project, add it to your `INSTALLED_APPS`:

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
