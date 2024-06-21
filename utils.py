import os

import database as dbs

db = dbs.Database(sqlite_path="brain_game.db")

def hide_st(st):
    dev = os.getenv("DEV")
    if dev:
        return
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def check_player_credential(username, password):
    db.set_query("SELECT id FROM player WHERE username = ? AND password = ?", (username, password))
    records = db.execute_query(False)
    return records


def insert_new_player(name, type, username, password):
    try:
        db.set_query("SELECT * FROM player WHERE username = ?", (username,))
        user_exists = db.execute_query(False)
        if not user_exists:
            db.set_query("INSERT INTO player (name, type, username, password) VALUES (?, ?, ?, ?)", (name, type, username, password))
            db.execute_query()
            return True
        else:
            return False
    except Exception as err:
        print(err)
        return False


def get_game_types():
    db.set_query("SELECT * FROM game_types")
    records = db.execute_query(False)
    return records


def save_history_guessing(game_history_id, player_id, guess, correct_numbers, correct_positions):
    db.set_query(
        "INSERT INTO guesses (game_history_id, player_id, guess, correct_numbers, correct_positions) VALUES (?, ?, ?, ?, ?)",
        (game_history_id, player_id, guess, correct_numbers, correct_positions)
    )
    db.execute_query()


def create_new_game(player_id, game_type_id):
    db.set_query(
        "INSERT INTO game_histories (player_id, game_id, game_level_id) VALUES (?, ?, ?)",
        (player_id, game_type_id, 1)
    )
    db.execute_query()
    db.set_query("SELECT MAX(id) FROM game_histories")
    records = db.execute_query(False)
    return records


def get_guessing_history_current_game(game_history_id, player_id):
    query = """
    SELECT g.guess, g.correct_numbers, g.correct_positions 
    FROM guesses AS g
    JOIN game_histories AS gh ON gh.id = g.game_history_id
    JOIN player AS p ON p.id = g.player_id
    WHERE p.id = ? AND gh.id = ?
    """
    db.set_query(query, (player_id, game_history_id))
    results = db.execute_query(False)
    return results


def get_total_guessing_in_one_game(game_history_id, player_id):
    query = """
    SELECT COUNT(*)
    FROM guesses AS g
    JOIN game_histories AS gh ON gh.id = g.game_history_id
    JOIN player AS p ON p.id = g.player_id
    WHERE p.id = ? AND gh.id = ?
    """
    db.set_query(query, (player_id, game_history_id))
    results = db.execute_query(False)
    return results


def get_leaderboard():
    query = """
    SELECT p.name, COUNT(*) AS skor, gh.game_date
    FROM guesses AS g
    JOIN game_histories AS gh ON gh.id = g.game_history_id
    JOIN player AS p ON p.id = g.player_id
    GROUP BY p.name, gh.game_date
    ORDER BY gh.game_date ASC
    """
    db.set_query(query)
    results = db.execute_query(False)
    return results








def initial_db():
    # Membuat tabel player
    create_player_table = """
    CREATE TABLE IF NOT EXISTS player (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NULL,
        type TEXT NULL,
        username TEXT NULL,
        password TEXT NULL
    );
    """
    db.set_query(create_player_table)
    db.execute_query()

    # Membuat history tebakan
    create_guess_table = """
    CREATE TABLE IF NOT EXISTS guesses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_history_id INTEGER NOT NULL,
        player_id INTEGER NOT NULL,
        guess TEXT NOT NULL,
        correct_numbers INTEGER NOT NULL,
        correct_positions INTEGER NOT NULL
    );
    """
    db.set_query(create_guess_table)
    db.execute_query()

    # Membuat table game
    create_game_table = """
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_type_id INTEGER NOT NULL,
        game_name TEXT NOT NULL
    );
    """
    db.set_query(create_game_table)
    db.execute_query()

    # Membuat table game type
    create_game_type_table = """
    CREATE TABLE IF NOT EXISTS game_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_type_name TEXT NOT NULL
    );
    """
    db.set_query(create_game_type_table)
    db.execute_query()

    # Membuat table game level
    create_game_level_table = """
    CREATE TABLE IF NOT EXISTS game_levels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_level_name TEXT NOT NULL
    );
    """
    db.set_query(create_game_level_table)
    db.execute_query()

    # Membuat tabel history
    create_history_table = """
    CREATE TABLE IF NOT EXISTS game_histories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id INTEGER NOT NULL,
        game_id INTEGER NOT NULL,
        game_level_id INTEGER NOT NULL,
        game_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        score INTEGER
    );
    """
    db.set_query(create_history_table)
    db.execute_query()

    # Membuat tabel leaderboard
    create_leaderboard_table = """
    CREATE TABLE IF NOT EXISTS leaderboard (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id INTEGER NULL,
        score INTEGER NULL
    );
    """
    db.set_query(create_leaderboard_table)
    db.execute_query()







def initial_records():
    # insert multiple game type
    db.set_query(
        """
        INSERT INTO game_types (game_type_name) 
        VALUES ('number'), ('letter'), ('words')
        """
    )
    db.execute_query()

    # insert multiple games
    db.set_query(
        """
        INSERT INTO games (game_type_id, game_name) 
        VALUES (1, 'Bulls and Cows'), (2, 'Hangman'), (3, 'Scrambled Words')
        """
    )
    db.execute_query()

    #insert multiple game levels    
    db.set_query(
        """
        INSERT INTO game_levels (game_level_name) 
        VALUES ('Easy'), ('Medium'), ('Hard')
        """
    )
    db.execute_query()

    #insert admin account
    db.set_query(
        """
        INSERT INTO player (name, type, username, password) 
        VALUES ('Rizumiya', 'admin', 'rend', 'ray')
        """
    )
    db.execute_query()

