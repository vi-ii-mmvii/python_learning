import psycopg2
import json
from config import db_config


# Database connection
def connect():
    try:
        return psycopg2.connect(**db_config)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


# Create table
def create_table():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(30),
            surname VARCHAR(30),
            phone VARCHAR(15)
        )
    """)
    conn.commit()
    conn.close()


# Insert from console using stored procedure
def insert_from_console():
    while True:
        print("\n[Insert Data]")
        name = input("Enter name (or 'q' to quit): ")
        if name.lower() == 'q':
            break
        surname = input("Enter surname (or 'q' to quit): ")
        if surname.lower() == 'q':
            break
        phone = input("Enter phone (or 'q' to quit): ")
        if phone.lower() == 'q':
            break
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("CALL insert_or_update_user(%s, %s, %s)",
                       (name, surname, phone))
        conn.commit()
        print("User inserted/updated.")
        conn.close()


# Search by pattern using function
def search_by_pattern():
    pattern = input("\nEnter pattern to search (in name/surname/phone): ")
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM search_phonebook(%s)", (pattern,))
    rows = cursor.fetchall()
    if rows:
        print("\n[Search Results]")
        print(f"{'ID':<5} {'Name':<15} {'Surname':<15} {'Phone':<15}")
        print("-" * 50)
        for row in rows:
            row = [value if value is not None else "" for value in row]
            print(f"{row[0]:<5} {row[1]:<15} {row[2]:<15} {row[3]:<15}")
    else:
        print("No results found.")
    conn.close()


# Paginated view
def view_paginated():
    try:
        limit = int(input("Enter limit: "))
        offset = int(input("Enter offset: "))
    except ValueError:
        print("Limit and offset must be numbers.")
        return
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM get_paginated_phonebook(%s, %s)", (limit, offset))
    rows = cursor.fetchall()
    if rows:
        print("\n[Paginated Results]")
        print(f"{'ID':<5} {'Name':<15} {'Surname':<15} {'Phone':<15}")
        print("-" * 50)
        for row in rows:
            row = [str(val) if val is not None else "" for val in row]
            print(f"{row[0]:<5} {row[1]:<15} {row[2]:<15} {row[3]:<15}")
    else:
        print("No records found.")
    conn.close()


# Delete using stored procedure
def delete_by_value():
    value = input("Enter name/surname/phone to delete: ")
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("CALL delete_by_name_or_phone(%s)", (value,))
    conn.commit()
    conn.close()
    print(f"Records with value '{value}' deleted.")


# Clear table
def clear_table():
    print("\n[Clear Table]")
    confirm = input("Are you sure you want to clear the table? (yes/no): ")
    if confirm.lower() == "yes":
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM phonebook")
        conn.commit()
        conn.close()
        print("Table cleared.")
    else:
        print("Operation canceled.")


# Main menu
def main():
    create_table()
    while True:
        print("\n[PhoneBook Menu]")
        print("[1] Insert User(s)")
        print("[2] Search by Pattern")
        print("[3] View Paginated Records")
        print("[4] Delete by Name/Surname/Phone")
        print("[5] Clear Table")
        print("[q] Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            insert_from_console()
        elif choice == "2":
            search_by_pattern()
        elif choice == "3":
            view_paginated()
        elif choice == "4":
            delete_by_value()
        elif choice == "5":
            clear_table()
        elif choice.lower() == "q":
            print("Exiting PhoneBook. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
