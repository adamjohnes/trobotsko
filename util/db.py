from mysql.connector import pooling
from dotenv import load_dotenv
import os
from datetime import datetime
import json
from logs.logging import load_logs_config

load_dotenv()
logging = load_logs_config()

def create_pool():
  return pooling.MySQLConnectionPool(
    pool_name     = "bot_pool",
    pool_size     = 5,                 # tweak for your load
    pool_reset_session = True,
    host          = os.getenv("DB_HOST"),
    port          = 3306,
    user          = os.getenv("DB_USER"),
    password      = os.getenv("DB_PASS"),
    database      = os.getenv("DB_NAME"),
    use_pure      = True
  )

def get_conn(pool):
  class _ConnCtx:
    def __enter__(self):
      self.conn = pool.get_connection();
      return self.conn
    def __exit__(self, exc_type, exc, tb):
      self.conn.close()
  return _ConnCtx()

def perform_query(pool, message, query, values):
  with pool.get_connection() as conn:
    print(message)
    cur = conn.cursor()
    cur.execute(
      query,
      (values)
    )
    conn.commit()
        
# def ensure_user(pool, user):
#   with pool.get_connection() as conn:
#     cur = conn.cursor()
#     cur.execute(
#       """
#       INSERT IGNORE INTO users (id, username, rsn, created_at)
#       VALUES (%s, %s, %s, %s)
#       """,
#       (user.id, user.name, None, datetime.now())
#     )
#     conn.commit()

# def update_rsn(pool, user, rsn):
#   with pool.get_connection() as conn:
#     print(f"[DB] Updating RSN for {user.id} → {rsn}")
#     cur = conn.cursor()
#     cur.execute(
#       "UPDATE users SET rsn=%s WHERE id=%s",
#       (rsn, user.id)
#     )
#     conn.commit()
    
def create_playlist_db(pool, user, playlist):
  with pool.get_connection() as conn:
    print(f"[DB] Creating playlist for {user.id} → {playlist}")
    cur = conn.cursor()
    cur.execute(
      """
      INSERT IGNORE INTO playlists (user_id, name, created_at, user)
      VALUES (%s, %s, %s, %s)
      """,
      (user.id, playlist, datetime.now(), user.name)
    )
    conn.commit()
    
def select_playlist_db(pool, user):
  with pool.get_connection() as conn:
    print(f"[DB] Selecting playlists for {user.id}")
    cur = conn.cursor()
    cur.execute(
      """
      SELECT name, songs FROM playlists WHERE user_id=%s
      """,
      (user.id,)
    )
    
    results = cur.fetchall()
    # Build a dictionary where keys = playlist names, values = list of songs
    playlist_dict = {}

    for name, songs in results:
      if songs:
        playlist_dict[name.lower()] = json.loads(songs)
      else:
        playlist_dict[name.lower()] = []  # Handle playlists with no songs

    return playlist_dict
  
def insert_song_db(pool, user, playlist, song):
  with pool.get_connection() as conn:
    print(f"[DB] Attempting to add {song} to {playlist} for: {user.id}")
    cur = conn.cursor()

    # First, get the current song list
    cur.execute(
      "SELECT songs FROM playlists WHERE user_id=%s AND name=%s",
      (user.id, playlist)
    )
    results = cur.fetchone()

    if results is None:
      print(f"No playlist found for user {user.id} and playlist '{playlist}'")
      return

    try:
      if results[0]:
        existing_songs = json.loads(results[0])
      else:
        existing_songs = []
    except Exception as e:
      print(f"Error parsing songs: {e}")
      existing_songs = []

    # Append new song
    existing_songs.append(song)

    # Update the songs column
    cur.execute(
      """
      UPDATE playlists
      SET songs=%s
      WHERE user_id=%s AND name=%s
      """,
      (json.dumps(existing_songs), user.id, playlist)
    )
    conn.commit()
    
def remove_song_db(pool, user, playlist, song):
  with pool.get_connection() as conn:
    print(f"[DB] Attempting to remove {song} from {playlist} for: {user.id}")
    cur = conn.cursor()

    # First, get the current song list
    cur.execute(
      "SELECT songs FROM playlists WHERE user_id=%s AND name=%s",
      (user.id, playlist)
    )
    results = cur.fetchone()

    if results is None:
      print(f"No playlist found for user {user.id} and playlist '{playlist}'")
      return

    try:
      if results[0]:
        existing_songs = json.loads(results[0])
      else:
        print(f"No songs exist in playlist: {playlist}.")
        return
    except Exception as e:
      print(f"Error parsing songs: {e}")

    # Remove song
    try:
      existing_songs.remove(song)
    except Exception as e:
      print(f"Could not find song: {e}")
      return False

    # Update the songs column
    cur.execute(
      """
      UPDATE playlists
      SET songs=%s
      WHERE user_id=%s AND name=%s
      """,
      (json.dumps(existing_songs), user.id, playlist)
    )
    conn.commit()
    return True
  
def insert_file_db(pool, user, fileElements):
  with pool.get_connection() as conn:
    logging.info(f"[DB] Creating file metadata for {user.id} → {fileElements}")
    cur = conn.cursor()
    cur.execute(
      """
      INSERT IGNORE INTO userfiles (user_id, filename, accessname, localpath, created_at)
      VALUES (%s, %s, %s, %s, %s)
      """,
      (user.id, fileElements["fileName"], fileElements["accessName"], fileElements["savedPath"], datetime.now())
    )
    conn.commit()

def see_file_db(pool, user):
  with pool.get_connection() as conn:
    logging.info(f"[DB] Fetching file metadata for {user.id}")
    cur = conn.cursor()
    cur.execute(
      """
      SELECT filename, accessname, localpath, created_at FROM userfiles WHERE user_id=%s
      """,
      (user.id,)
    )
    results = cur.fetchall()
    filesMetadata = []
    for filename, accessname, localpath, created_at in results:
      filesMetadata.append({
        "filename": filename,
        "accessname": accessname,
        "localpath": localpath,
        "created_at": str(created_at)
      })
    return filesMetadata
  
def delete_file_db(pool, user, accessName):
  with pool.get_connection() as conn:
    logging.info(f"[DB] Attempting to delete file {accessName} for {user.id}")
    cur = conn.cursor()
    cur.execute(
      """
      DELETE FROM userfiles WHERE user_id=%s and accessname=%s
      """,
      (user.id, accessName)
    )
    conn.commit()