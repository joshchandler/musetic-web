Musetic
=======

Organization
------------

This is a Django project (1.7) Commands can be run with manage.py

Settings are in musetic/settings/

Installation
------------
Setup ::

    $ git clone git@bitbucket.org:<your_fork>/musetic-web.git
    $ cd musetic-web
    $ git remote add upstream git@bitbucket.org:musetic/musetic-web.git

    $ virtualenv -p python3 env
    $ . ./env/bin/activate
    $ pip install -r requirements/base.txt
    $ python manage.py migrate
    $ python manage.py collectstatic


Modification
------------

To add an app, perform the following commands ::

    $ cd musetic-web
    $ . ./env/bin/activate
    $ mkdir -p musetic/apps/<app-name>
    $ touch musetic/apps/__init__.py
    $ python manage.py startapp <app-name> ./musetic/apps/<app-name>

    Then add to INSTALLED_APPS settings/base.py

    ```
    INSTALLED_APPS = (
        ...
        '<app-name>',
        ...
    )
    ```

Then run the command to create the database entries::

    $ python manage.py makemigrations <app-name>
    $ python manage.py migrate


Running a test server
---------------------

To use your application in development, use `runserver_plus` from the
django_extensions suite. ::

    $ python manage.py runserver_plus 0.0.0.0:8000


Loading Test Data
-----------------
Fixtures are placed in each application, and they will have to be loaded manually::
    
#### User application ####
    $ python manage.py loaddata musetic/apps/user/fixtures/*

#### Submission application ####
    $ python manage.py loaddata musetic/apps/submission/fixtures/*


Tests
-----

To run the tests, run the run_tests.sh script ::

    $ ./run_tests.sh

This will also run flake8 for static code analysis. Please
follow [Google's python style](http://google-styleguide.googlecode.com/svn/trunk/pyguide.html)
guide wherever possible


Running Specific Tests
--------------
If you don't want to run the entire test suite when you're creating tests,

You can narrow your tests::
    
    $ python manage.py test musetic.apps.user.tests.test_views.UserViewTests


Application Logging
-------------------

In order to print out helpful messages for debugging or otherwise, please avoid
using `print` and use python's built-in logging like so. ::

    ```
    from django.http import Http404

    import logging
    LOG = logging.get_logger(__name__)

    def login(request):
        user = request.GET['user']
        try:
            User.objects.get(username=user)
        except User.DoesNotExist:
            LOG.error('User {0} does not exist'.format(user))
            raise Http404
    ```

In settings, `logging.py` has already been pre configured that all messages INFO
and above will go to stdout, and DEBUG will be ignored. See
[Python's logging documentation](https://docs.python.org/2/library/logging.html)
for more details.


Authors
-------
- Joshua Chandler <joshchandler88@gmail.com>
- Micah Hausler <hausler.m@gmail.com>
