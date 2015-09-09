web: newrelic-admin run-program gunicorn musetic.wsgi --log-file -
celeryworker: celery worker -A musetic -l INFO
celerybeat: celery beat -A musetic 