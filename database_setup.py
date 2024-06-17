import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to {db_file}")
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def setup_database():
    database = "word_guessing_game.db"

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                    id integer PRIMARY KEY,
                                    username text NOT NULL UNIQUE,
                                    target_word text,
                                    guess_count integer DEFAULT 0
                                 ); """

    sql_create_guesses_table = """ CREATE TABLE IF NOT EXISTS guesses (
                                    id integer PRIMARY KEY,
                                    user_id integer NOT NULL,
                                    guess text NOT NULL,
                                    score real NOT NULL,
                                    FOREIGN KEY (user_id) REFERENCES users (id)
                                 ); """

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_users_table)
        create_table(conn, sql_create_guesses_table)
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    setup_database()
