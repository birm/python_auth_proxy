from dotenv import load_dotenv  # pip package python-dotenv
import os
from flask import request, Response, make_response
import requests
import jwt
import datetime
import make_keys
import bcrypt

app = flask.Flask(__name__)
flask_cors.CORS(app)

# encode/decode default to utf-8, FYI

# JWT signing RSA keys
PUBKEY_FILE = "key.pub"
PRIKEY_FILE = "key"
# make private and public keys if not exist
if not (os.path.isfile(PRIKEY_FILE) and  os.path.isfile(PUBKEY_FILE)):
    make_keys(PRIKEY_FILE, PUBKEY_FILE)

# load pubkey and prikey

private_key = open(PRIKEY_FILE).read()
public_key = open(PUBKEY_FILE).read()

# create sqlite user db if not exists
user_db = sqlite3.connect("users.db")
user_cur = user_db.cursor()
user_cur.execute("""CREATE TABLE IF NOT EXISTS user (
username TEXT primary key,
salt TEXT,
hash TEXT
)""")
user_db.commit()

load_dotenv()
API_HOST = os.environ.get('API_HOST', "localhost:8000")

def get_file(filename):
    try:
        src = os.path.join(path.abspath(os.path.dirname(__file__)), filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)

def check_login(username, password):
    if not username or not password:
        return False
    else:
        sql_str = "select username, salt, hash from user where username = (?)"
        res = user_cur.execute(sql_str, username)
        x = res.fetchone()
        if (x):
            un, salt, db_hash = x
            # recompute and compare hash
            hashed = bcrypt.hashpw(str.encode(password), str.encode(salt))
            if db_hash == hashed:
                return True
            else:
                return False
        else:
            # no such user
            return False

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'token' in request.cookies:
            token = request.cookies.get(token)
            # passing user for likely future audit logs
            user = None
            try:
                data = jwt.decode(encoded, public_key, algorithms=["RS256"])
                user = data.get("sub")
            except jwt.exceptions.InvalidTokenError as e:
                # if token is bad, don't route
                print(repr(e))
                return make_response(jsonify({"message": "Invalid token!", "error": repr(e)}), 401)
                # TODO redirect instead
            return f(user, *args, **kwargs)
        else:
            # if token is missing don't route, but explain how this works
            return make_response(jsonify({"message": "Token from ./login expected in cookie with name token"}), 401)
            # TODO redirect instead
    return decorator

@api.route('/login', methods = ['POST'])
def loginHandler():
    # get username and password
    data = request.get_json()
    username = data.get("username", False)
    password = data.get("password", False)
    ## TODO if login ok
    if (check_login(username, password)):
        # set expiry
        exp = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=1)
        # make and return token
        token = jwt.encode({"sub": username, "exp": exp}, private_key, algorithm="RS256")
        return {"token": token}
    else:
        return {"error": "Invalid login"}
    pass

@api.route("/login.html")
def loginFile():
    content = get_file('login.html')
    return Response(content, mimetype="text/html")

@token_required
@api.route('/', defaults={'path': ''})
@api.route('/<path>')
def redirect_to_API_HOST(path):
    res = requests.request(
        method          = request.method,
        url             = request.url.replace(request.host_url, f'{API_HOST}/'),
        headers         = {k:v for k,v in request.headers if k.lower() == 'host'},
        data            = request.get_data(),
        cookies         = request.cookies,
        allow_redirects = False,
    )

    # exlcude some keys in :res response
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        (k,v) for k,v in res.raw.headers.items()
        if k.lower() not in excluded_headers
    ]

    response = Response(res.content, res.status_code, headers)
    return response
