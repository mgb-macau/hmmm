from os import getenv

import pymysql
from pymysql.err import OperationalError

# TODO(developer): specify SQL connection details
CONNECTION_NAME = getenv(
  'INSTANCE_CONNECTION_NAME',
  'nordcloud:us-central1:ncdbsql')
DB_USER = getenv('MYSQL_USER', 'root')
DB_PASSWORD = getenv('MYSQL_PASSWORD', '')
DB_NAME = getenv('MYSQL_DATABASE', 'newtestdb')

mysql_config = {
  'user': DB_USER,
  'password': DB_PASSWORD,
  'db': DB_NAME,
  'charset': 'utf8mb4',
  'cursorclass': pymysql.cursors.DictCursor,
  'autocommit': True
}

# Create SQL connection globally to enable reuse
# PyMySQL does not include support for connection pooling
mysql_conn = None


def __get_cursor():
    """
    Helper function to get a cursor
      PyMySQL does NOT automatically reconnect,
      so we must reconnect explicitly using ping()
    """
    try:
        return mysql_conn.cursor()
    except OperationalError:
        mysql_conn.ping(reconnect=True)
        return mysql_conn.cursor()


def mysql_demo(request):
    global mysql_conn
    email1="this@email.add"
    pwd1="mypass"
    # Initialize connections lazily, in case SQL access isn't needed for this
    # GCF instance. Doing so minimizes the number of active SQL connections,
    # which helps keep your GCF instances under SQL connection limits.
    if not mysql_conn:
        try:
            mysql_conn = pymysql.connect(**mysql_config)
        except OperationalError:
            # If production settings fail, use local development ones
            mysql_config['unix_socket'] = f'/cloudsql/{CONNECTION_NAME}'
            mysql_conn = pymysql.connect(**mysql_config)

    # Remember to close SQL resources declared while running this function.
    # Keep any declared in global scope (e.g. mysql_conn) for later reuse.
    with __get_cursor() as cursor:
        # cursor.execute('SELECT NOW() as now')
        sqlcode1 = "INSERT INTO users (email, password) VALUES (%s, %s)"
        myvals = (email1, pwd1)
        # cursor.execute(sqlcode1, myvals)
        cursor.execute('SELECT * FROM users')
        # results = cursor.fetchone()
        makeform = "<form action='/action_page.php'>  First name: <input type='text' name='fname'><br>  Last name: <input type='text' name='lname'><br>  <input type='submit' value='Submit'></form>"
        results = cursor.fetchall()
        return "<html><h1>WELCOME!!!</h1><br>" + str(results) + makeform
