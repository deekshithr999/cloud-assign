import sqlite3
from flask import Flask, render_template, g, request,redirect, url_for
import os

#PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

#DATABASE = os.path.join(PROJECT_ROOT, 'flaskapp', 'tmpdb1.db')

DATABASE = '/var/www/html/flaskapp/users.db'
UPLOAD_FOLDER = 'uploads'
app = Flask(__name__)
app.config.from_object(__name__)

#...


#conn = sqlite3.connect('tmpdb1.db')
#cur = conn.cursor()
#cur.execute("""DROP TABLE IF EXISTS entries""")
#cursor.execute('''CREATE TABLE IF NOT EXISTS your_table_name (id INTEGER PRIMARY KEY, name TEXT)''')



def connect_to_database():
        return sqlite3.connect(app.config['DATABASE'])

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def execute_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

def commit():
    get_db().commit()



@app.route('/')
def mainpage():
    return render_template('mainpage.html')


@app.route('/submit', methods=['POST'])
def submit():
    # Retrieve form data
    username = request.form['username']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']

    #print("====================>", password, first_name)
    # Store the information in the database
    #conn = sqlite3.connect('user_info.db')
    #cursor = conn.cursor()
    #cursor.execute('''
    #    INSERT INTO users (username, password, first_name, last_name, email)
    #    VALUES (?, ?, ?, ?, ?)
    #''', (username, password, first_name, last_name, email))
    #conn.commit()
    #conn.close()
    CREATE_TABLE =  '''
                        CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        first_name TEXT,
                        last_name TEXT,
                        email TEXT
                         )
                    '''
    INSERT_INTO_TABLE = '''
                                INSERT INTO users (username, password, first_name, last_name, email)
                                VALUES (?, ?, ?, ?, ?)
                        '''
    CHECK_USER = ''' SELECT * FROM users WHERE username=? '''
    execute_query(CREATE_TABLE)
    nfile = request.files['textfile']
    wc = None #default val
    if nfile:
         wc = cntWords(nfile)

    print("debug word count === ", wc)

    print("=================hereee1========")
    user_exists = execute_query(CHECK_USER, (username))
    commit()
    print("=============here2=========")
    print("res from user exists", user_exists)
    if user_exists: 
        if user_exists[0][1] != password:
            return render_template('mainpage.html', error='Invalid Credentials')
        return redirect(url_for('display_details', username=username, password=password, wc=wc))


    res = execute_query(CREATE_TABLE)
    print("res from db create", res)
    commit()
    if username is None or password is None or first_name is None or last_name is None or email is None:
        print("========================= here") 
        return render_template('mainpage.html', error='Enter all Details !!')
    res = execute_query(INSERT_INTO_TABLE, (username, password, first_name, last_name, email))
    print("res from db insert", res)
    commit()
    # Redirect to a page displaying all details
    return redirect(url_for('display_details', username=username, password=password, wc=wc))


@app.route('/display_details')
def display_details():
    # Retrieve information from the database based on the provided username and password
    username = request.args.get('username')
    password = request.args.get('password')
    wc = request.args.get('wc')

    #conn = sqlite3.connect('user_info.db')
    #cursor = conn.cursor()
    #cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    #user_info = cursor.fetchone()
    #conn.close()
    FETCH_DETAILS = '''
			SELECT * FROM  users  WHERE  username=? AND password=?
		    '''
    user_inf=execute_query(FETCH_DETAILS, (username, password))
    commit()
    print("res from db fetch user_inf", user_inf)
    return render_template('display_details.html', user_info=user_inf, wc=wc)


def cntWords(nfile):
    string = nfile.read()
    words = string.split()
    return str(len(words))


if __name__ == '__main__':
       app.run(debug=True)
