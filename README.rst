Vimcar backend API coding challenge
====================================

Vimcar backend application by Szabolcs Antal.


Quickstart
----------



First run the following commands to bootstrap your environment ::

    git clone https://github.com/kamforka/vimcar-backend-challenge
    cd vimcar-backend-challenge
    pip install -r requirements/dev.txt

Then set the ``FLASK_APP`` and ``FLASK_DEBUG``
environment variables ::

    export FLASK_APP=/path/to/autoapp.py
    export FLASK_DEBUG=1

To create the sqlite database instance type the following ::

    flask db init
    flask db migrate
    flask db upgrade

Also you might need to set up different credentials for the mailing service. In order to do that
you should override the below configurations in the ``settings.py`` file ::

    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = 'a9b27dbd9c4f39'
    MAIL_PASSWORD = 'ffbab59f515653'
    MAIL_DEFAULT_SENDER = 'noreply@vimcar.de'

Now you can start up the application ::

    flask run

Your app will be served at http://127.0.0.1:5000/ by default.

Features
--------

- Register user
- Confirm user registration
- Get user by id (authentication required)
- Get user list (authentication required)
- Update a user (authentication required)


User Registration
.................

To regiser a user, just make a POST request to the `/api/users/` endpoint with the email and password fields ::

    curl -X POST http://127.0.0.1:5000/api/users -d email=foo@bar.com -d password=bar

You will get a response like this ::

    {
        "active": false,
        "email": "foo@bar.com",
        "id": 1
    }
    
Confirm registration
....................

As you can see from the previous response the state of the user is inactive by default, so to activate it you should navigate to the mail server you set up for development and click the activation link sent by the API.

To check whether the activation was successful or not you can retrieve the user by id.

Get user by id
..............

In order to get a user from the API you must make a request to the `/api/users/<user_id>` endpoint with Basic authentication credentials, for simplicity you can use the `email` and the `password` of any registered user. ::

    curl -u foo@bar.com:bar -X GET http://127.0.0.1:5000/api/users/1 

If everything went fine during the registration and activation you will probably get a similiar response as below ::

    {
        "active": true,
        "email": "foo@bar.com",
        "id": 1
    }
    
Quite the same as before, but now the user is activated.


Get list of users
.................

You can also get the full list of registered users by making a `GET` request to the `/api/users` endpoint. Not to mention you still need authentication to pass. ::

    curl -u foo@bar.com:bar -X GET http://127.0.0.1:5000/api/users
    
Update a user
.............

To update a single user you need to pass the key-value pairs of the fields that should be modified to the `/api/users/<user_id>` using a `PUT` request ::

    curl -u foo@bar.com:bar -X PUT http://127.0.0.1:5000/api/users/1 -d password=foobar

As a response you will get the updated instance ::

    {
        "active": true,
        "email": "bar@foo.com",
        "id": 1
    }


Shell
-----

To open the interactive shell, run ::

    flask shell

By default, you will have access to the flask ``app``, to the ``db`` instance and to the ``User`` model.

To manage the application`s users from the shell instead of the api ::

    >>> User.query.all()
    [<User('bar@foo.com')>]
    >>> user = User.query.filter_by(email="bar@foo.com").first()
    >>> user.email
    'bar@foo.com'
    >>> User.create(email="foo@foo.com")
    <User('foo@foo.com')>



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
