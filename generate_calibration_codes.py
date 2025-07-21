import random
import sqlite3

def insert_data_into_db(file_path):
    # Connect to the SQLite database
    conn = sqlite3.connect('calibrate_data.db')
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            uNum TEXT PRIMARY KEY,
            empName TEXT,
            passcode INTEGER
        )
    ''')

    # Read the output file and insert each row into the database
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:  # Skip empty lines
                uNum, empName, passcode = line.split(',')
                try:
                    cursor.execute('''
                        INSERT INTO users (uNum, empName, passcode)
                        VALUES (?, ?, ?)
                    ''', (uNum, empName, int(passcode)))
                except sqlite3.IntegrityError:
                    print(f"uNum {uNum} already exists — skipping")

    # Commit the transaction and close the connection
    conn.commit()
    cursor.close()
    conn.close()




def generate_random_code():
    """Generate a random 4-digit code."""
    return str(random.randint(1000, 9999))

def process_file(input_file, output_file):
    """Read the input file, append a random 4-digit code, and write to the output file."""
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if line:  # Skip empty lines
                u_number, name = line.split(',')
                random_code = generate_random_code()
                new_line = f"{u_number},{name},{random_code}\n"
                outfile.write(new_line)

if __name__ == "__main__":
    input_file = 'emp_name.txt'  # Replace with your input file name
    output_file = 'emp_name_with_codes.txt'  # Replace with your desired output file name
    # process_file(input_file, output_file)

    insert_data_into_db(output_file)