import sqlite3

# Open the text file for reading
with open('english_words.txt', 'r') as f:
  
  # Create a connection to the database
  conn = sqlite3.connect('english_words.db')
  
  # Create a cursor object to execute SQL commands
  cur = conn.cursor()
  
  # Create the table if not exists
  cur.execute('''CREATE TABLE IF NOT EXISTS words (
                  word TEXT,
                  length INTEGER
                );''')
  
  # Loop through each line in the file and insert into the table
  for word in f:
    # Calculate the length of the line
    word = word.strip()
    length = len(word)
    
    # Insert the line, word, and length into the table
    cur.execute("INSERT INTO words (word, length) VALUES (?, ?);", (word, length))
  
  # Commit the changes and close the database connection
  conn.commit()
  conn.close()
