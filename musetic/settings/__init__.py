import os


if 'DOCKER_DEV' in os.environ:
    settings_file = 'docker.py'
elif 'www' in os.path.abspath(__file__).split('/') or 'PRODUCTION' in os.environ:
    settings_file = 'production.py'
elif 'CI' in os.environ:
    settings_file = 'codeship.py'
else:
    settings_file = 'development.py'

settings_file_join = os.path.join(os.path.dirname(__file__), settings_file)

#http://stackoverflow.com/questions/6357361/alternative-to-execfile-in-python-3-2
exec(open(settings_file_join).read())
