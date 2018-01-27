===============================
Vimcar backend API coding challenge
===============================

Vimcar backend API coding challenge


Quickstart
----------

First, set your app's secret key as an environment variable. For example,
add the following to ``.bashrc`` or ``.bash_profile``.

.. code-block:: bash

    export VIMCAR_SECRET='something-really-secret'

Before running shell commands, set the ``FLASK_APP`` and ``FLASK_DEBUG``
environment variables ::

    export FLASK_APP=/path/to/autoapp.py
    export FLASK_DEBUG=1

Then run the following commands to bootstrap your environment ::

    git clone https://github.com/kamforka/vimcar
    cd vimcar
    pip install -r requirements/dev.txt

To create the sqlite database instance type the following ::

    flask db init
    flask db migrate
    flask db upgrade

Now you can start up the application ::

    flask run

Your app will be served on http://127.0.0.1:5000/ by default.

To explore the api, first create a user.
For this you can use a command line application like curl. ::

    curl -H "Content-type: application/json" -X POST -d '{"username":"foo", "password":"bar", "email":"foo@bar.com"}' http://127.0.0.1:5000/api/users

Then with your new user you can get an authentication token by ::

    curl -H "Content-type: application/json" -X POST -d '{"username":"foo", "password":"bar"}' http://127.0.0.1:5000/auth

The api will respond with an access token ::

    {
        "access_token": "eyJhbGciOiJIUzI1..."
    }

As the api uses JWT tokens for authentication, you can get the user list by requesting the users view with the token received ::

    curl -H "Authorization: JWT <access_token>" -X GET http://127.0.0.1:5000/api/users

If the provided token is valid the response will contain the list of users ::
    
    {
        "username": "foo",
        "id": 1,
        "email": "foo@bar.com"
    }


Shell
-----

To open the interactive shell, run ::

    flask shell

By default, you will have access to the flask ``app``, to the ``db`` instance and to the ``User`` model.

To manage the application`s users from the shell instead of the api ::

    >>> User.query.all()
    [<User (u'foo')>]
    >>> user = User.query.filter_by(username="foo").first()
    >>> user.email
    u'foo@bar.com'
    >>> User.create(username="phoo", email="phoo@oohp.com")
    <User (u'phoo')>


Running Tests
-------------

To run all tests, run ::

    flask test


Migrations
----------

Whenever a database migration needs to be made. Run the following commands ::

    flask db migrate

This will generate a new migration script. Then run ::

    flask db upgrade

To apply the migration.

For a full migration command reference, run ``flask db --help``.
