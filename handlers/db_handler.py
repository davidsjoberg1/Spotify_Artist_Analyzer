import sqlite3


def create_tables(conn, cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS all_artists (
                   artist_id text PRIMARY KEY,
                   name text,
                   popularity integer,
                   followers integer,
                   is_searched boolean
                       )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS artist_relationships (
                   artist_id TEXT REFERENCES all_artists(artist_id),
                   related_artist_id TEXT REFERENCES all_artists(artist_id),
                   PRIMARY KEY (artist_id, related_artist_id)
                 )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS genre_relationships (
                   artist_id text REFERENCES all_artists(artist_id),
                   genre text,
                   PRIMARY KEY (artist_id, genre)
                   )''')
    conn.commit()


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
    data_lst = [(artist_id, related_artist["id"]) for related_artist in related_artists]
    cursor.executemany(f'''INSERT OR REPLACE INTO artist_relationships
                    (artist_id, related_artist_id)
                    VALUES (?, ?)''',
                    data_lst)
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


def delete_artist(table, artist_id, conn, cursor):
    cursor.execute(f"DELETE FROM {table} WHERE artist_id = {artist_id}")
    conn.commit()


def delete_table(table_name, conn, cursor):
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()


def get_table_length(table, cursor):
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    return count


def get_first_not_searched_artist(cursor):
    cursor.execute(f"SELECT * FROM all_artists WHERE is_searched = 0 LIMIT 1")
    artist = cursor.fetchone()
    return artist

def get_artist(artist_id, cursor):
    cursor.execute(f"SELECT * FROM all_artists WHERE artist_id = '{artist_id}'")
    artist = cursor.fetchone()
    return artist


def get_all(table, cursor):
    cursor.execute(f"SELECT * FROM {table}")
    artists = cursor.fetchall()
    return artists


def get_all_searched(is_searched, cursor):
    cursor.execute(f"SELECT * FROM all_artists WHERE is_searched = {is_searched}")
    artists = cursor.fetchall()
    return artists


def get_all_searched_count(is_searched, cursor):
    cursor.execute(f"SELECT COUNT(*) FROM all_artists WHERE is_searched = {is_searched}")
    count = cursor.fetchone()[0]
    return count


def get_all_genres(cursor):
    cursor.execute(f"SELECT DISTINCT genre FROM genre_relationships")
    genres = cursor.fetchall()
    return genres

def get_related_artists(artist_id, cursor):
    cursor.execute(f"SELECT related_artist_id FROM artist_relationships WHERE artist_id = '{artist_id}'")
    related_artists = cursor.fetchall()
    return related_artists

def get_all_artist_relationships(cursor):
    cursor.execute(f"SELECT * FROM artist_relationships")
    relationships = cursor.fetchall()
    return relationships

def get_1000_random_artists(cursor):
    cursor.execute(f"SELECT artist_id FROM all_artists WHERE is_searched = 1 ORDER BY RANDOM() LIMIT 1000")
    artists = cursor.fetchall()
    return artists

def get_first_100_artist_relationships(cursor):
    cursor.execute(f"SELECT * FROM artist_relationships LIMIT 10000")
    relationships = cursor.fetchall()
    return relationships

    

