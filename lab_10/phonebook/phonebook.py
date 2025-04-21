import psycopg2

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


# Insert data from CSV
def insert_from_csv(file_path):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "COPY phonebook (name, surname, phone) "
        f"FROM '{file_path}' "
        "DELIMITER ',' "
        "CSV HEADER")
    cursor.execute("""
        DELETE FROM phonebook a
        USING phonebook b
        WHERE a.id > b.id
        AND a.name = b.name
        AND a.surname = b.surname
        AND a.phone = b.phone
    """)
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
        cursor.execute(
            "SELECT COUNT(*) FROM phonebook WHERE name = %s AND surname = %s AND phone = %s",
            (name, surname, phone))
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO phonebook (name, surname, phone) "
                "VALUES (%s, %s, %s)", (name, surname, phone))
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
            cursor.execute("UPDATE phonebook SET name = %s WHERE id = %s",
                           (new_name, user_id))
        elif choice == "2":
            new_surname = input("Enter new surname: ")
            cursor.execute("UPDATE phonebook SET surname = %s WHERE id = %s",
                           (new_surname, user_id))
        elif choice == "3":
            new_phone = input("Enter new phone: ")
            cursor.execute("UPDATE phonebook SET phone = %s WHERE id = %s",
                           (new_phone, user_id))
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
            filter_name = input("Enter name to filter: ")
            cursor.execute(
                "SELECT * FROM phonebook WHERE name = %s", (filter_name,))
        elif choice == "2":
            filter_surname = input("Enter surname to filter: ")
            cursor.execute(
                "SELECT * FROM phonebook WHERE surname = %s", (filter_surname,))
        elif choice == "3":
            filter_phone = input("Enter phone to filter: ")
            cursor.execute(
                "SELECT * FROM phonebook WHERE phone = %s", (filter_phone,))
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
        cursor.execute("DELETE FROM phonebook WHERE id = %s", (_id,))
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
        print("[5] Delete Data by Name")
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
