import sqlite3
from sqlite3 import Error

# Function to create a connection to the SQLite database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to SQLite database: {db_file}")
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

# Function to create the table
def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_finances (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                total_money REAL DEFAULT 0,
                total_hours_worked REAL DEFAULT 0,
                UNIQUE(user_id)
            )
        ''')
        print("Table 'user_finances' created successfully.")
    except Error as e:
        print(f"Error creating table: {e}")

# Function to insert or update user data
def update_user_finances(conn, user_id, money_earned=0, hours_worked=0):
    try:
        cursor = conn.cursor()
        # Check if the user already exists
        cursor.execute('SELECT * FROM user_finances WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()

        if user:
            # Update existing user
            new_total_money = user[2] + money_earned
            new_total_hours = user[3] + hours_worked
            cursor.execute('''
                UPDATE user_finances
                SET total_money = ?, total_hours_worked = ?
                WHERE user_id = ?
            ''', (new_total_money, new_total_hours, user_id))
        else:
            # Insert new user
            cursor.execute('''
                INSERT INTO user_finances (user_id, total_money, total_hours_worked)
                VALUES (?, ?, ?)
            ''', (user_id, money_earned, hours_worked))

        conn.commit()
        print(f"Updated finances for user {user_id}.")
    except Error as e:
        print(f"Error updating user finances: {e}")

# Function to fetch user data
def get_user_finances(conn, user_id):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user_finances WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        if user:
            print(f"User ID: {user[1]}, Total Money: {user[2]}, Total Hours Worked: {user[3]}")
            return user
        else:
            print(f"No data found for user {user_id}.")
            return None
    except Error as e:
        print(f"Error fetching user finances: {e}")

# Function to get user input
def get_user_input():
    try:
        user_id = int(input("Enter your user ID: "))
        money_earned = float(input("Enter the amount of money earned: "))
        hours_worked = float(input("Enter the number of hours worked: "))
        return user_id, money_earned, hours_worked
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return None, None, None
    
    
def clear_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM user_finances')
        conn.commit()
        print("All rows deleted from the table.")
    except Error as e:
        print(f"Error clearing table: {e}")

# Main function to demonstrate usage
def main():
    database = "user_finances.db"

    # Create a database connection
    conn = create_connection(database)
    if conn is not None:
        # Create the table
        create_table(conn)

        # Get user input
        user_id, money_earned, hours_worked = get_user_input()
        if user_id is not None and money_earned is not None and hours_worked is not None:
            # Update user finances
            update_user_finances(conn, user_id, money_earned, hours_worked)

            # Fetch and display user finances
            get_user_finances(conn, user_id)

        # Close the connection
        clear_table(conn)
        conn.close()
    else:
        print("Error: Could not connect to the database.")

if __name__ == '__main__':
    main()