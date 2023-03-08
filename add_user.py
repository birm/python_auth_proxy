import sqlite3
import bcrypt

username = "something"
password = "something else"

salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(str.encode(password), salt)
print(salt, hashed)

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
