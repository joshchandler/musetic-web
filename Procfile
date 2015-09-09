web: newrelic-admin run-program gunicorn musetic.wsgi --log-file -
worker: newrelic-admin run-program celery worker -A musetic -l INFO
beat: newrelic-admin run-program celery beat -A musetic -l INFO 