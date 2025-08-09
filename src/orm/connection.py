import mysql.connector
from mysql.connector import errorcode

# Authentication info
config = {
    "user": "ORM",
    "password": "strongpassword123",
    "host": "127.0.0.1",
    "port": 3306,
    "database": "ORMDB",
    "raise_on_warnings": True,
}


def run_query(sql: str, params=None, return_last_id=False):
    """
    Execute the given SQL statement.
    Give it you'r SQL statement and it will execute it in mysql server that is running on your machine.
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)

        if sql.strip().lower().startswith("select"):
            return cursor.fetchall()
        else:
            conn.commit()
            if return_last_id:
                return cursor.lastrowid
            else:
                return cursor.rowcount

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            msg = "Invalid credentials"
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            msg = "Database does not exist"
        else:
            msg = f"MySQL error [{err.errno}]: {err.msg}"
        raise RuntimeError(msg)

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()


if __name__ == "__main__":
    try:
        # Example SELECT
        sql = "SELECT * FROM users"
        results = run_query(sql)
        if results:
            for row in results:
                print(row)
        else:
            print("No rows returned.")

        # Example INSERT with last insert id
        insert_sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
        last_id = run_query(
            insert_sql, params=("mmd", "mmd@domain.com"), return_last_id=True
        )
        print(f"Inserted row ID: {last_id}")

    except RuntimeError as e:
        print(f"Error running SQL:\n  {e}")
