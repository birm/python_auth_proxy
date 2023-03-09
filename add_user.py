import sqlite3
import bcrypt
import getpass

user = input("Username [%s]: " % getpass.getuser())
if not user:
    user = getpass.getuser()

pprompt = lambda: (getpass.getpass(), getpass.getpass('Retype password: '))

p1, p2 = pprompt()
while p1 != p2:
    print('Passwords do not match. Try again')
    p1, p2 = pprompt()

username = user
password = p1

salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(str.encode(password), salt)

# create sqlite user db if not exists
user_db = sqlite3.connect("users.db")
user_cur = user_db.cursor()
user_cur.execute("""CREATE TABLE IF NOT EXISTS user (
username TEXT primary key,
salt TEXT,
hash TEXT
)""")

sql_str = "insert into user (username, salt, hash) values (?, ?, ?)"
user_cur.execute(sql_str, (username, salt.decode(), hashed.decode()))
user_db.commit()
