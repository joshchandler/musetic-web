web: newrelic-admin run-program gunicorn musetic.wsgi --log-file -
celeryworker: celery worker --app=musetic -l INFO
celerybeat: celery beat --app=musetic