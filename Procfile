web: newrelic-admin run-program gunicorn musetic.wsgi --log-file -
celery-worker: celery worker --app=musetic -l INFO
celery-beat: celery beat --app=musetic