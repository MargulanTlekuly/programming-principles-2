import psycopg2
import csv
from config import load_config

def create_table():
    """ Creates all required tables for the lab (phone_book, game_users, scores). """
    commands = (
        """
        CREATE TABLE IF NOT EXISTS phone_book (
            contact_id SERIAL PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255),
            phone_number VARCHAR(20) NOT NULL UNIQUE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS game_users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            level INT NOT NULL DEFAULT 1
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS scores (
            score_id SERIAL PRIMARY KEY,
            user_id INT NOT NULL,
            score INT NOT NULL,
            saved_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id)
                REFERENCES game_users (user_id)
                ON DELETE CASCADE
        )
        """
    )
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Database error: {error}")
def insert_from_csv(file_path):
    """ Inserts data from a CSV file. """
    sql = "INSERT INTO phone_book(first_name, last_name, phone_number) VALUES (%s, %s, %s) ON CONFLICT (phone_number) DO NOTHING;"
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader)
                    for row in reader:
                        if row: cur.execute(sql, row)
        print(f"Data from {file_path} loaded successfully.")
    except Exception as error:
        print(f"Error while loading from CSV: {error}")

def insert_from_console():
    """ Inserts a new contact from user input. """
    print("\nEnter new contact details:")
    first_name = input("First Name: ")
    last_name = input("Last Name (optional): ")
    phone_number = input("Phone Number: ")
    if not first_name or not phone_number:
        print("First name and phone number are required. Contact not added.")
        return
    sql = "INSERT INTO phone_book(first_name, last_name, phone_number) VALUES (%s, %s, %s)"
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (first_name, last_name, phone_number))
        print("Contact added successfully!")
    except Exception as error:
        print(f"Could not add contact: {error}")

def query_contacts():
    """ Queries contacts with an optional filter. """
    filter_term = input("\nEnter name or phone to search (leave blank to show all): ")
    if filter_term:
        sql = "SELECT contact_id, first_name, last_name, phone_number FROM phone_book WHERE first_name ILIKE %s OR last_name ILIKE %s OR phone_number ILIKE %s"
        params = (f"%{filter_term}%", f"%{filter_term}%", f"%{filter_term}%")
    else:
        sql = "SELECT contact_id, first_name, last_name, phone_number FROM phone_book ORDER BY first_name"
        params = None
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                rows = cur.fetchall()
                if not rows: print("No contacts found.")
                else:
                    print("\n--- Search Results ---")
                    for row in rows: print(f"ID: {row[0]}, Name: {row[1]} {row[2]}, Phone: {row[3]}")
    except Exception as error:
        print(f"Query failed: {error}")

def update_contact():
    """ Updates an existing contact's first name or phone number. """
    search_term = input("Enter the first name of the contact to update: ")
    new_first_name = input("Enter new first name (or leave blank): ")
    new_phone = input("Enter new phone number (or leave blank): ")

    if not new_first_name and not new_phone:
        print("Nothing to update.")
        return

    query_parts = []
    params = []
    if new_first_name:
        query_parts.append("first_name = %s")
        params.append(new_first_name)
    if new_phone:
        query_parts.append("phone_number = %s")
        params.append(new_phone)
    
    params.append(search_term)
    
    sql = f"UPDATE phone_book SET {', '.join(query_parts)} WHERE first_name = %s"
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, tuple(params))
                if cur.rowcount == 0: print("Contact not found.")
                else: print(f"Successfully updated {cur.rowcount} contact(s).")
    except Exception as error:
        print(f"Update failed: {error}")

def delete_contact():
    """ Deletes a contact by their first name or phone number. """
    identifier = input("\nEnter first name or phone number to delete: ")
    sql = "DELETE FROM phone_book WHERE first_name = %s OR phone_number = %s"
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (identifier, identifier))
                if cur.rowcount == 0: print("Contact not found.")
                else: print(f"Successfully deleted {cur.rowcount} contact(s).")
    except Exception as error:
        print(f"Delete failed: {error}")

def main_menu():
    create_table()
    print("Welcome! Select a program to run.")
    while True:
        print("\n===== Main Menu =====")
        print("1. Open Phone Book")
        print("2. Start Snake Game")
        print("exit - to close the program")
        
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            phone_book_menu() 
        elif choice == '2':
            start_game_session()
        elif choice.lower() == 'exit':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def phone_book_menu():
    """ Menu for Phone Book. """
    while True:
        print("\n--- Phone Book ---")
        print("1. Search contacts")
        print("2. Add new contact")
        print("3. Update a contact")
        print("4. Delete a contact")
        print("5. Load data from contacts.csv")
        print("back - to return to main menu")
        
        choice = input("Enter your choice: ").strip()

        if choice == '1': query_contacts()
        elif choice == '2': insert_from_console()
        elif choice == '3': update_contact()
        elif choice == '4': delete_contact()
        elif choice == '5': insert_from_csv('contacts.csv')
        elif choice.lower() == 'back':
            break
        else:
            print("Invalid choice.")


# --- НОВЫЕ ФУНКЦИИ ДЛЯ ИГРЫ "ЗМЕЙКА" ---

def get_or_create_user(username):
    """
    Находит пользователя по имени. Если не найден, создает нового.
    Возвращает данные пользователя (id, username, level).
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT user_id, username, level FROM game_users WHERE username = %s", (username,))
                user_data = cur.fetchone() # fetchone() получает одну строку результата
                
                if user_data:
                    print(f"Welcome back, {user_data[1]}! Your current level is {user_data[2]}.")
                    return user_data
                else:
                    print(f"User '{username}' not found. Creating a new profile.")
                    # RETURNING - команда PostgreSQL, которая возвращает данные только что созданной строки
                    cur.execute("INSERT INTO game_users (username) VALUES (%s) RETURNING user_id, username, level;", (username,))
                    new_user_data = cur.fetchone()
                    print(f"Welcome, {new_user_data[1]}! You are starting at level {new_user_data[2]}.")
                    return new_user_data
    except Exception as error:
        print(f"User operation failed: {error}")
        return None

def save_score(user_id, score):
    sql = "INSERT INTO scores (user_id, score) VALUES (%s, %s)"
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (user_id, score))
        print(f"Score {score} saved for user_id {user_id}.")
    except Exception as error:
        print(f"Failed to save score: {error}")


def start_game_session():
    username = input("Enter your username to start the game: ")
    user_info = get_or_create_user(username)

    if not user_info:
        print("Could not start the game. Exiting.")
        return

    user_id = user_info[0]
    current_score = 0

    print("\n--- Game Started! ---")
    print("Commands: '+' to score points, 'p' to pause and save, 'q' to quit.")
    
    # Это симуляция игрового цикла
    while True:
        action = input(f"Current score: {current_score}. Your action: ").strip()
        
        if action == '+':
            current_score += 10
            print("+10 points!")
        elif action.lower() == 'p':
            print("Game paused. Saving current state...")
            save_score(user_id, current_score)
        elif action.lower() == 'q':
            break
        else:
            print("Unknown command.")
            
    print(f"\nGame over! Your final score: {current_score}")
    save_score(user_id, current_score) 

if __name__ == '__main__':
    main_menu()