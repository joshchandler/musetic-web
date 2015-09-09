web: newrelic-admin run-program gunicorn musetic.wsgi --log-file -
worker: celery worker --app=musetic -l INFO
worker: celery beat --app=musetic --schedular=djcelery.schedulers.DatabaseScheduler