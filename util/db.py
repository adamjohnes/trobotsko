from mysql.connector import pooling
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

def create_pool():
  return pooling.MySQLConnectionPool(
    pool_name     = "bot_pool",
    pool_size     = 5,                 # tweak for your load
    pool_reset_session = True,
    host          = "localhost",
    user          = os.getenv("DB_USER"),
    password      = os.getenv("DB_PASS"),
    database      = os.getenv("DB_NAME"),
  )

def get_conn(pool):
  class _ConnCtx:
    def __enter__(self):
      self.conn = pool.get_connection();
      return self.conn
    def __exit__(self, exc_type, exc, tb):
      self.conn.close()
  return _ConnCtx()


def ensure_user(pool, user):
  with pool.get_connection() as conn:
    cur = conn.cursor()
    cur.execute(
      """
      INSERT IGNORE INTO users (id, username, rsn, created_at)
      VALUES (%s, %s, %s, %s)
      """,
      (user.id, user.name, None, datetime.now())
    )
    conn.commit()

def update_rsn(pool, user, rsn):
  with pool.get_connection() as conn:
    print(f"[DB] Updating RSN for {user.id} → {rsn}")
    cur = conn.cursor()
    cur.execute(
      "UPDATE users SET rsn = %s WHERE id = %s",
      (rsn, user.id)
    )
    conn.commit()