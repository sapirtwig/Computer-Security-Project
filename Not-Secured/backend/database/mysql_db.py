import pymysql

# Function to establish a database connection
def get_db_connection():
    return pymysql.connect(
        host="mysql",
        user="root",
        password="password",
        database="project",
        client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS  # Allows multiple SQL statements
    )

# Function to get a database connection using a context manager (yield)
def get_db():
    db = get_db_connection()
    try:
        yield db
    finally:
        db.close()  # Ensure the database connection is closed after use

# Function to create tables in the database
def create_tables():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Creating the 'users' table
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    );
    """
    cursor.execute(create_users_table)

    # Creating the 'clients' table
    create_clients_table = """
    CREATE TABLE IF NOT EXISTS clients (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """
    cursor.execute(create_clients_table)

    print("Tables created successfully.")
    connection.commit()  # Save changes to the database
    cursor.close()
    connection.close()  # Close the database connection
