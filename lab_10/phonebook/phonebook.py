import sqlite3
import csv


# Database connection
def connect():
    return sqlite3.connect("phonebook.db")


# Create table
def create_table():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            surname TEXT,
            phone TEXT
        )
    """)
    conn.commit()
    conn.close()


# Insert data from CSV
def insert_from_csv(file_path):
    conn = connect()
    cursor = conn.cursor()
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("""
                SELECT COUNT(*) FROM phonebook
                WHERE name = ? AND surname = ? AND phone = ?
            """, (row['name'], row['surname'], row['phone']))
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO phonebook (name, surname, phone)
                    VALUES (?, ?, ?)
                """, (row['name'], row['surname'], row['phone']))
    conn.commit()
    conn.close()


# Insert data from console
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
        cursor.execute("""
            SELECT COUNT(*) FROM phonebook
            WHERE name = ? AND surname = ? AND phone = ?
        """, (name, surname, phone))
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO phonebook (name, surname, phone)
                VALUES (?, ?, ?)
            """, (name, surname, phone))
            conn.commit()
            print("Record inserted successfully.")
        else:
            print("Duplicate record found. Skipping insertion.")
        conn.close()


# Update data
def update_data():
    print("\n[Update Data]")
    user_id = input("Enter ID to update: ")
    conn = connect()
    cursor = conn.cursor()
    while True:
        print("\n[Update Options]")
        print("[1] Update Name")
        print("[2] Update Surname")
        print("[3] Update Phone")
        print("[q] Quit Update")
        choice = input("Choose an option: ")
        if choice == "1":
            new_name = input("Enter new name: ")
            cursor.execute("UPDATE phonebook SET name = ? WHERE id = ?", (new_name, user_id))
        elif choice == "2":
            new_surname = input("Enter new surname: ")
            cursor.execute("UPDATE phonebook SET surname = ? WHERE id = ?", (new_surname, user_id))
        elif choice == "3":
            new_phone = input("Enter new phone: ")
            cursor.execute("UPDATE phonebook SET phone = ? WHERE id = ?", (new_phone, user_id))
        elif choice.lower() == "q":
            break
        else:
            print("Invalid choice. Try again.")
    conn.commit()
    conn.close()


# Query data
def query_data():
    print("\n[Query Data]")
    conn = connect()
    cursor = conn.cursor()
    while True:
        print("\n[Query Options]")
        print("[1] Filter by Name")
        print("[2] Filter by Surname")
        print("[3] Filter by Phone")
        print("[4] Show All Records")
        print("[q] Quit Query")
        choice = input("Choose an option: ")
        if choice == "1":
            value = input("Enter name: ")
            cursor.execute("SELECT * FROM phonebook WHERE name = ?", (value,))
        elif choice == "2":
            value = input("Enter surname: ")
            cursor.execute("SELECT * FROM phonebook WHERE surname = ?", (value,))
        elif choice == "3":
            value = input("Enter phone: ")
            cursor.execute("SELECT * FROM phonebook WHERE phone = ?", (value,))
        elif choice == "4":
            cursor.execute("SELECT * FROM phonebook")
        elif choice.lower() == "q":
            break
        else:
            print("Invalid choice. Try again.")
            continue

        rows = cursor.fetchall()
        if rows:
            print("\n[Query Results]")
            print(f"{'ID':<5} {'Name':<15} {'Surname':<15} {'Phone':<15}")
            print("-" * 50)
            for row in rows:
                row = [value if value is not None else "" for value in row]
                print(f"{row[0]:<5} {row[1]:<15} {row[2]:<15} {row[3]:<15}")

        else:
            print("No records found.")
    conn.close()


# Delete data
def delete_data():
    print("\n[Delete Data]")
    conn = connect()
    cursor = conn.cursor()
    while True:
        _id = input("Enter ID to delete (or 'q' to quit): ")
        if _id.lower() == 'q':
            break
        cursor.execute("DELETE FROM phonebook WHERE id = ?", (_id,))
        conn.commit()
        print(f"Record(s) with ID '{_id}' deleted.")
    conn.close()


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
        print("[1] Insert from CSV")
        print("[2] Insert from Console")
        print("[3] Update Data")
        print("[4] Query Data")
        print("[5] Delete Data by ID")
        print("[6] Clear Table")
        print("[q] Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            file_path = input("Enter CSV file path: ")
            insert_from_csv(file_path)
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_data()
        elif choice == "4":
            query_data()
        elif choice == "5":
            delete_data()
        elif choice == "6":
            clear_table()
        elif choice.lower() == "q":
            print("Exiting PhoneBook. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
