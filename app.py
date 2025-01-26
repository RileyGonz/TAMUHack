import sqlite3
from sqlite3 import Error
from datetime import datetime, date, timedelta


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
                hourly_wage REAL DEFAULT 0,
                expected_finances Real DEFAULT 0,
                planned_expenses REAL DEFAULT 0,
                bonuses_raises REAL DEFAULT 0,
                days_off REAL DEFAULT 0,
                payed_time_off_exceptions REAL DEFAULT 0,  
                curr_date TEXT DEFAULT ' ',
                exp_date TEXT DEFAULT ' ',
                UNIQUE(user_id)
            )
        ''')
        print("Table 'user_finances' created successfully.")
    except Error as e:
        print(f"Error creating table: {e}")



def update_user_finances(conn, user_id, money_earned=0, hours_worked=0, hourly_wage = 0, expected_finances = 0, planned_expenses = 0, bonuses_raises = 0, days_off = 0, payed_time_off_exceptions = 0, curr_date = " ", exp_date = " "):
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
                SET total_money = ?, total_hours_worked = ?, expected_finances = ?
                WHERE user_id = ?
            ''', (new_total_money, new_total_hours, expected_finances, user_id))
        else:
            # Insert new user if not found
            cursor.execute('''
                INSERT INTO user_finances (user_id, total_money, total_hours_worked, hourly_wage, expected_finances, planned_expenses, bonuses_raises, days_off, payed_time_off_exceptions, curr_date, exp_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, money_earned, hours_worked, hourly_wage, expected_finances, planned_expenses, bonuses_raises, days_off, payed_time_off_exceptions, curr_date, exp_date))

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
            print(f"User ID: {user[1]}, Total Money: {user[2]}, Total Hours Worked: {user[3]}, Hourly Wage: {user[4]},Expected Finances: {user[5]}, Planned Expenses: {user[6]}, Bonuses/Raises: {user[7]}, Days Off: {user[8]}, Payed Days Off: {user[9]}, Current date: {user[10]}, Expected Date: {user[11]}")
            return user
        else:
            print(f"No data found for user {user_id}.")
            return None
    except Error as e:
        print(f"Error fetching user finances: {e}")

def calculate_days_between_dates(date1_str, date2_str):
    try:
        date_format = "%b%d"
        date1 = datetime.strptime(date1_str, date_format)
        date2 = datetime.strptime(date2_str, date_format)
        delta = date2 - date1
        return delta.days
    except ValueError as e:
        print(f"Error: {e}. Please ensure the dates are in the correct format.")
        return None

# Function to get user input
def get_user_input():
    try:
        user_id = int(input("Enter your user ID: "))
        money_earned = float(input("Enter the amount of money earned: "))
        hours_worked = float(input("Enter the number of hours worked: "))
        hourly_wage = float(input("Enter the hourly wage: "))
        expected_finances = float(input("Enter the number of expected finances: "))
        planned_expenses = float(input("Enter the number of planned expanses: "))
        bonuses_raises = float(input("Enter the number of bonus raises: "))
        days_off = int(input("Enter the number of days off: "))
        payed_time_off_exceptions = int(input("Enter the number of payed days off: "))
        curr_date = input("Enter the current date: ").strip()
        exp_date = input("Enter the expected date: ").strip()

        return user_id, money_earned, hours_worked, hourly_wage, expected_finances, planned_expenses, bonuses_raises, days_off, payed_time_off_exceptions, curr_date, exp_date
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

def main():
    database = "user_finances.db"

    # Create a database connection
    conn = create_connection(database)
    if conn is not None:
        # Create the table if it doesn't exist
        create_table(conn)

        #add_exp_date_column(conn)

        # Get user input for finances
        user_id, money_earned, hours_worked, hourly_wage, expected_finances, planned_expenses, bonuses_raises, days_off, payed_time_off_exceptions, curr_date, exp_date = get_user_input()

        if user_id is not None and money_earned is not None and hours_worked is not None:
            # Perform calculations
            total_money = money_earned
            total_hours_worked = hours_worked
            new_total_money = total_money + total_money  # example update for current balance

            print(f"Current total money: {new_total_money}")
            expected_expenses = new_total_money * 0.08
            print(f"Expected expenses: {expected_expenses}")

            # Ask user if they have expected finances
            answer = input("Do you have expected finances? Enter Y/N: ").strip().upper()
            if answer == "Y":
                expected_expenses = new_total_money * 0.08  # example: adjust based on actual logic
                finances = (hourly_wage * hours_worked) - expected_expenses
                new_total_money = finances - expected_finances  # update money after expected expenses
            elif answer == "N":
                finances = hourly_wage * hours_worked
                new_total_money = finances
                print(f"Calculated finances without expected expenses: {new_total_money}")
            else:
                print("Invalid input. Please enter 'Y' or 'N'.")
                return

            # Call the function to update user finances in the database
            update_user_finances(conn, user_id, new_total_money, hours_worked, hourly_wage, expected_finances, planned_expenses, bonuses_raises, days_off, payed_time_off_exceptions, curr_date, exp_date)

            # Fetch and display updated user finances
            get_user_finances(conn, user_id)

        # Clear table and close connection after all operations
        clear_table(conn)
        conn.close()
    else:
        print("Error: Could not connect to the database.")

if __name__ == '__main__':
    main()