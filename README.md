# python_auth_proxy

## How it works
Relays proxy requests to a specific host iff a valid JWT is in the request cookie named "token".

This also exposes one static file, /login.html as a usable reference on how to handle login from a browser application. To use otherwise, post to /handleLogin with a json containing username and password (and appropriate content type header) to get a token back.

The app creates ./key and ./key.pub if these are not present.

User information is stored in a sqlite3 db at ./user.db, which is created if not present. This contains (username, salt, hash). Don't trust the salted hash too much, and don't reuse passwords. Please. Not just here, don't reuse passwords.

Tokens expire after one hour.

Username is in "sub".

This does not have the usual openid-connect discovery/others endpoints.

## Running
To install dependencies, run something like `python3 -m pip3 install -r requirements.txt`

To start the server, run something like `python3 -m gunicorn -w 4 -b 0.0.0.0:4000 server:app --timeout 400`

You can add a user in a shell with `add_user.py`.

The API_HOST is an enviroment variable which can be passed as a .env if needed. This defaults to localhost:8000.

The REDIRECT_URL is used to generate redirect messages, and should be something like "http://special-server.com/login.html"

I've added a Dockerfile for convenience, but this may have unintended consequences, as each worker in a k8s environment may generate different keys. Configure carefully.

Using a python virtualenv is probably fine.
