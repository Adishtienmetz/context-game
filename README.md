***Context Word Guessing Game***

**Overview**

Welcome to the Word Guessing Game!
This game challenges players to guess a randomly generated target word based on semantic similarity.
The closer your guess is to the target word in meaning, the higher your score.

**Features**

- *User Registration and Login:* Register a new user or log in with an existing username.

- *Guessing System:* Make guesses and receive scores based on semantic similarity to the target word.

- *Score Tracking:* Keep track of your best guesses and the total number of guesses made.

- *Database Integration:* All user data and guesses are stored in an SQLite database.

***Installation***

  **Requirements**
  - Python 3.x
  - spaCy (en_core_web_md model)
  - Faker
  - SQLite3

  **Setup**
  - Clone the repository
  - Run: pip install spacy faker; python -m spacy download en_core_web_md
  - Run the database script: python database_setup.py
  - Run the main file: python main.py
  - Start playing!
