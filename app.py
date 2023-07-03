from flask import Flask, render_template, g
import sqlite3
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.database = 'products.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_PERMANENT'] = False

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.database)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Registering blueprints
from routes import index, cart, checkout
app.register_blueprint(index.bp)
app.register_blueprint(cart.bp)
app.register_blueprint(checkout.bp)

if __name__ == '__main__':
    app.run(debug=True)