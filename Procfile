web: newrelic-admin run-program gunicorn musetic.wsgi --log-file -
worker: newrelic-admin run-program celery worker --app=musetic --loglevel=INFO --autoreload
beat: newrelic-admin run-program celery beat --app=musetic --loglevel=INFO