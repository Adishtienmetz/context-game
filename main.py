import spacy
import sqlite3
from database_setup import create_connection
from faker import Faker

nlp = spacy.load('en_core_web_md')

database = "word_guessing_game.db"

fake = Faker()

def register_user(conn, username):
    sql = ''' INSERT INTO users(username)
              VALUES(?) '''
    cur = conn.cursor()
    try:
        cur.execute(sql, (username,))
        conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError:
        print(f"Username {username} already taken. Please choose a different username.")
        return None

def login_user(conn, username):
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username=?", (username,))
    user = cur.fetchone()
    return user[0] if user else None

def insert_guess(conn, user_id, guess, score):
    cur = conn.cursor()
    cur.execute("SELECT id FROM guesses WHERE user_id=? AND guess=?", (user_id, guess))
    existing_guess = cur.fetchone()

    if existing_guess is None:
        sql = ''' INSERT INTO guesses(user_id, guess, score)
                  VALUES(?,?,?) '''
        cur.execute(sql, (user_id, guess, score))
        conn.commit()

# resets the game and the data about the user in the database
def reset_game(conn, user_id):
    target_word = fake.word()
    cur = conn.cursor()
    cur.execute("UPDATE users SET target_word=? WHERE id=?", (target_word, user_id))
    
    cur.execute("DELETE FROM guesses WHERE user_id=?", (user_id,))
    
    conn.commit()
    
    print("Game reset! Try to guess the new word.")
    
    return target_word

def fetch_top_guesses(conn, user_id):
    cur = conn.cursor()
    cur.execute("SELECT guess, score FROM guesses WHERE user_id=? ORDER BY score DESC LIMIT 5", (user_id,))
    return cur.fetchall()

def semantic_similarity(word1, word2):
    token1 = nlp(word1)
    token2 = nlp(word2)
    return token1.similarity(token2)

def get_or_generate_target_word(conn, user_id):
    cur = conn.cursor()
    cur.execute("SELECT target_word FROM users WHERE id=?", (user_id,))
    result = cur.fetchone()
    if result and result[0]:
        return result[0]
    else:
        target_word = fake.word()
        cur.execute("UPDATE users SET target_word=? WHERE id=?", (target_word, user_id))
        conn.commit()
        return target_word

conn = create_connection(database)

print("Welcome to the Word Guessing Game!")
print("Do you have an account? (yes/no)")
has_account = input().strip().lower()

user_id = None
if has_account == 'yes':
    while user_id is None:
        username = input("Enter your username: ").strip()
        if(username == 'sign up'):
            while user_id is None:
                username = input("Choose a username: ").strip()
                user_id = register_user(conn, username)
        else:
            user_id = login_user(conn, username)
            if user_id is None:
                print("Username not found. Try again or type 'sign up' to register.")
else:
    while user_id is None:
        username = input("Choose a username: ").strip()
        user_id = register_user(conn, username)

print(f"Welcome, {username}!")
print("Try to guess the target word based on its semantic similarity.")
print("You can type 'quit' to exit the game, or 'reveal' to see the answer!")
print('---------------------------------------------------')

target_word = get_or_generate_target_word(conn, user_id)

while True:
    guess = input("Enter your guess: ").strip().lower()
    if guess == "quit":
        print("Thanks for playing! Goodbye!")
        break
    elif guess == "reveal":
        print(f"The answer was: {target_word}")
    elif guess == "reset":
        target_word = reset_game(conn, user_id)
    elif guess == target_word:
        print('Congratulations! You guessed the word correctly!')
        target_word = reset_game(conn, user_id)
    else:
        score = 100 * semantic_similarity(target_word, guess)
        print(f"Guess score: {score:.2f}")
        insert_guess(conn, user_id, guess, score)
        top_guesses = fetch_top_guesses(conn, user_id)
        print('Top 5 Best Guesses:')
        for num, (g, s) in enumerate(top_guesses, 1):
            print(f"{num}. {g}, score: {s:.2f}")
        print('---------------------------------------------------')

if conn:
    conn.close()
