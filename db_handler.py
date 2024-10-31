import sqlite3

def create_tables():
    conn = sqlite3.connect('artists.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS all_artists (
                   artist_id text PRIMARY KEY,
                   name text,
                   popularity integer,
                   followers integer,
                   is_searched boolean
                       )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS artist_relationships (
                   artist_id text PRIMARY KEY REFERENCES all_artists(artist_id),
                   related_artists text
                       )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS genre_relationships (
                   id integer PRIMARY KEY AUTOINCREMENT,
                   artist_id text REFERENCES all_artists(artist_id),
                   genre text
                   )''')
    conn.commit()
    conn.close()


def insert_artist_data(data_lst, table, conn, cursor):
    insert_data = [(
        data["id"], 
        data["name"], 
        data["popularity"], 
        data["followers"],
        data["is_searched"]) for data in data_lst]
    cursor.executemany(f'''INSERT OR REPLACE INTO {table} 
                   (artist_id, name, popularity, followers, is_searched) 
                   VALUES (?, ?, ?, ?, ?)''', insert_data)
    
    insert_genre_relationships(data_lst, conn, cursor)
    conn.commit()



def insert_related_artists(artist_id, related_artists, conn, cursor):
    related_artists_data = [(artist_id, related_artist["id"]) for related_artist in related_artists]
    cursor.executemany(f'''INSERT OR REPLACE INTO artist_relationships
                       (artist_id, related_artists) 
                       VALUES (?, ?)''',
                       related_artists_data)
    conn.commit()


        

def insert_genre_relationships(data_lst, conn, cursor):
    genre_data =[(data["id"], genre) for data in data_lst for genre in data["genres"]]
    cursor.executemany(f'''INSERT OR REPLACE INTO genre_relationships
                       (artist_id, genre) 
                       VALUES (?, ?)''',
                       genre_data)
    conn.commit()



def set_is_searched(artist_id, is_searched, conn, cursor):
    cursor.execute(f'''UPDATE all_artists 
                       SET is_searched = {is_searched} 
                           WHERE artist_id = "{artist_id}"''')
    conn.commit()



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


def get_table_length(table):
    conn = sqlite3.connect('artists.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_first_not_searched_artist(cursor):
    cursor.execute(f"SELECT * FROM all_artists WHERE is_searched = 0 LIMIT 1")
    artist = cursor.fetchone()
    return artist

def get_artist(artist_id, cursor):
    cursor.execute(f"SELECT * FROM all_artists WHERE artist_id = '{artist_id}'")
    artist = cursor.fetchone()
    return artist


def get_all(table):
    conn = sqlite3.connect('artists.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    artists = cursor.fetchall()
    conn.close()
    return artists


def get_all_searched(is_searched, cursor):
    cursor.execute(f"SELECT * FROM all_artists WHERE is_searched = {is_searched}")
    artists = cursor.fetchall()
    return artists


def get_all_genres():
    conn = sqlite3.connect('artists.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT DISTINCT genre FROM genre_relationships")
    genres = cursor.fetchall()
    conn.close()
    return genres

    

