import config
import json
import requests
import sqlite3

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask import g, jsonify, request, render_template
from requests.exceptions import HTTPError


app = Flask(__name__)
app.config['DEBUG'] = True

DATABASE = 'rates.db'


@app.route('/')
def home():
    # send static html fiel
    # exchange rate updates in page
    return render_template('index.html') #TODO: this is a placeholder
    pass

@app.route('/api/rate/<quote>', methods=['GET'])
def latest_rate(quote):
    return str(query_latest_rate(quote))

@app.route('/api/rate', methods=['GET'])
def api_rate():
    print('REQUEST:  ',request.args)
    parameters = request.args
    currency = parameters.get('currency')

    if currency:
        rate = query_latest_rate(currency)
        return jsonify(rate)

@app.route('/ping')
def ping():
    return 'pong'

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


def query_latest_rate(quote):
    row = query_latest_row(quote)
    rate = row[0][2] #TODO: create class for currency rates
    return rate

def query_latest_row(quote=None):
    """
    Pull the latest rates from the database

    :param str quote: currency quote
    """
    quote_query = ''
    if quote:
        quote_query = f"WHERE quote = '{quote}'"

    query = f"""
            SELECT MAX(ts), quote, rate 
            FROM rates 
            {quote_query}
            GROUP BY quote
            """
    return query_db(query)

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
    data = pull_latest_rate_data()
    ts = data['timestamp']
    formatted = [(ts, currency, rate) for currency, rate in data['quotes'].items()]

    try:
        with app.app_context():
            conn = get_db()
            cur = conn.cursor()
            cur.executemany('INSERT INTO rates(ts, quote, rate) VALUES (?,?,?)', formatted)
            conn.commit()
    except Exception as err:
        print('ERROR:',err)
    finally:
        conn.close()
        # TODO: does it add duplicates??

def pull_latest_rate_data():
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
"""
    print(query_db('SELECT MAX(ts), quote, rate FROM rates GROUP BY quote'))

with app.app_context():
    print(query_latest_row())
    print('\n',query_latest_rate('KRW'))
"""
if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_db, 'interval', hours=1)
    scheduler.start()

    #Start Flask
    app.run(debug=True)
    """
    update_db()
    with app.app_context():
        print(query_latest_row())
        print('\n',query_latest_rate('KRW'))
        """
