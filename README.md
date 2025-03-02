# SkillSync_demo

1. Celery installations - To install celery and their related packages.
   1.
           1. pip install celery.
           2. pip install redis (message broker),
           3. pip install eventlet (by default celery works on prefork concurrency model which might not be suitable for windows
                   Installing eventlet forces Celery to use a green-threaded model.)
           celery -A <inner_project_name> worker -l info -P eventlet (command to start celery)
       make sure redis is installed in your machine and it is up and running.


3. Core - Create a celery.py file in core directory.
    Add the basic settings of celery which were provided in celery docs.


4. Settings - Add the settings of celery like message_broker url, backend, accept content, result serializer and task serializer
    into the settings.py file.


5. Async task creation - To create task async use .delay and .apply_async method to make the method handles by celery.


6. Handle async task - Create the task folder and module for appropriate async task handling,
    To make task to be handle asynchronously use @shared_task decorator from celery module.
