import sqlite3

def create_tables():
    conn = sqlite3.connect('artists.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS all_artists (
                       artist_id text PRIMARY KEY,
                       name text,
                       popularity integer,
                       followers integer
                       )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS search_artists (
                       artist_id text PRIMARY KEY,
                       name text,
                       popularity integer,
                       followers integer
                       )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS artist_relationships (
                       artist_id text PRIMARY KEY, 
                       related_artists text
                       )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS genre_relationships (
                        id integer PRIMARY KEY AUTOINCREMENT,
                        artist_id text,
                        genre text
                        )''')
    conn.commit()
    conn.close()

def insert_artist_data(data_lst, table):
    conn = sqlite3.connect('artists.db')
    cursor = conn.cursor()
    for data in data_lst:
        cursor.execute(f'''INSERT OR REPLACE INTO {table} 
                       (artist_id, name, popularity, followers) 
                           VALUES (?, ?, ?, ?)''',
                           (data["id"], 
                            data["name"], 
                            data["popularity"], 
                            data["followers"]))
    conn.commit()
    conn.close()
    insert_genre_relationships(data["id"], data["genres"])

def insert_related_artists(artist_id, related_artists):
    conn = sqlite3.connect('artists.db')
    cursor = conn.cursor()
    for related_artist in related_artists:
        # TODO skicak in related artists id ller hela skite???
        cursor.execute(f'''INSERT OR REPLACE INTO artist_relationships 
                       (artist_id, related_artists) 
                           VALUES (?, ?)''',
                           (artist_id, related_artist))
    conn.commit()
    conn.close()
        
def insert_genre_relationships(artist_id, genres):
    conn = sqlite3.connect('artists.db')
    cursor = conn.cursor()
    for genre in genres:
        cursor.execute(f'''INSERT INTO genre_relationships
                       (artist_id, genre) 
                           VALUES (?, ?)''',
                           (artist_id, genre))
    conn.commit()
    conn.close()
    
def get_table_length(table):
    conn = sqlite3.connect('artists.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_first_artist(table):
    conn = sqlite3.connect('artists.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table} LIMIT 1")
    artist = cursor.fetchone()
    conn.close()
    return artist

def delete_artist(table, artist_id):
    conn = sqlite3.connect('artists.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table} WHERE artist_id = {artist_id}")
    conn.commit()
    conn.close()

def delete_table(table_name):
    conn = sqlite3.connect('artists.db')
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()
    conn.close()
