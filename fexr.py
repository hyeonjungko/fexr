import config
import json
import requests
import sqlite3

from flask import Flask
from flask import g, request, render_template
from requests.exceptions import HTTPError


app = Flask(__name__)
app.config['DEBUG'] = True

DATABASE = 'rates.db'


@app.route('/')
def home():
    # send static html fiel
    # exchange rate updates in page
    pass

@app.route('/api', methods=['GET'])
def rate():
    print('REQUEST:\n',request.args)
    return render_template('index.html', rate=1123.44)

@app.route('/ping')
def ping():
    return 'pong'


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def update_db():
    """
    Update database with latest exchange rate data
    Run hourly
    """
    data = pull_latest_rates()
    ts = data['timestamp']
    formatted = [(ts, currency, rate) for currency, rate in data['quotes'].items()]

    with app.app_context():
        cur = get_db().cursor()
        cur.executemany('INSERT INTO rates(ts, quote, rate) VALUES (?,?,?)', formatted)

def pull_latest_rates():
    #TODO: move apikey from config to secrets.yaml when deploying to Kubernetes
    api_key = config.api_key
    url = f"http://apilayer.net/api/live?access_key={api_key}"
    r = requests.get(url) # wrap it in try-catch
    json = r.json()

    timestamp = json['timestamp']
    quotes = {key[-3:] : value for key, value in json['quotes'].items()}

    return {'timestamp':timestamp, 'quotes': quotes}

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """
    Initialize database using schema.sql
    """
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

#update_db()
