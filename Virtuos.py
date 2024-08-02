import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('example2.db')
cursor = conn.cursor()

# Create the students table
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    StudentName TEXT NOT NULL CHECK (length(StudentName) <= 30),
    CollegeName TEXT NOT NULL CHECK (length(CollegeName) <= 50),
    Round1Marks FLOAT NOT NULL CHECK (Round1Marks BETWEEN 0 AND 10),
    Round2Marks FLOAT NOT NULL CHECK (Round2Marks BETWEEN 0 AND 10),
    Round3Marks FLOAT NOT NULL CHECK (Round3Marks BETWEEN 0 AND 10),
    TechnicalRoundMarks FLOAT NOT NULL CHECK (TechnicalRoundMarks BETWEEN 0 AND 20),
    TotalMarks FLOAT NOT NULL CHECK (TotalMarks BETWEEN 0 AND 50),
    Result TEXT NOT NULL CHECK (Result IN ('Selected', 'Rejected')),
    Rank INTEGER NOT NULL
)
''')

conn.commit()

# Function to get valid input
def get_valid_input(prompt, min_val=None, max_val=None, max_length=None, is_numeric=False):
    while True:
        try:
            value = input(prompt)
            if max_length and len(value) > max_length:
                raise ValueError(f"Input cannot be longer than {max_length} characters.")
            if is_numeric:
                num_value = float(value)
                if (min_val is not None and num_value < min_val) or (max_val is not None and num_value > max_val):
                    raise ValueError(f"Input must be between {min_val} and {max_val}.")
                return num_value
            else:
                return value
        except ValueError as ve:
            print(ve)

# Take input from user
student_name = get_valid_input("Enter your name: ", max_length=30)
college_name = get_valid_input("Enter your college name: ", max_length=50)
round1_marks = get_valid_input("Enter your Round 1 marks: ", min_val=0, max_val=10, is_numeric=True)
round2_marks = get_valid_input("Enter your Round 2 marks: ", min_val=0, max_val=10, is_numeric=True)
round3_marks = get_valid_input("Enter your Round 3 marks: ", min_val=0, max_val=10, is_numeric=True)
technical_round_marks = get_valid_input("Enter your Technical Round marks: ", min_val=0, max_val=20, is_numeric=True)

# Calculate Total Marks
total_marks = round1_marks + round2_marks + round3_marks + technical_round_marks

# Determine Result
result = "Selected" if total_marks >= 35 else "Rejected"

# Insert data into the table
cursor.execute('''
INSERT INTO students (StudentName, CollegeName, Round1Marks, Round2Marks, Round3Marks, TechnicalRoundMarks, TotalMarks, Result, Rank)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
''', (student_name, college_name, round1_marks, round2_marks, round3_marks, technical_round_marks, total_marks, result))

conn.commit()

# Calculate Rank
cursor.execute('''
UPDATE students
SET Rank = (SELECT COUNT(*) FROM students s WHERE s.TotalMarks > students.TotalMarks) + 1
''')

conn.commit()

# Display all records sorted by rank
cursor.execute('SELECT * FROM students ORDER BY Rank ASC')
rows = cursor.fetchall()

print("\nID | Name | College | Round1 | Round2 | Round3 | TechRound | Total | Result | Rank")
for idx, row in enumerate(rows, start=1):
    print(f"{idx} | {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]} | {row[7]} | {row[8]}")

# Close the connection
conn.close()