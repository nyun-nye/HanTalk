from flask_mysqldb import MySQL

def init_db(mysql):
    cur = mysql.connection.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            student_id VARCHAR(100) UNIQUE NOT NULL,
            user_id VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)
    mysql.connection.commit()
    cur.close()
