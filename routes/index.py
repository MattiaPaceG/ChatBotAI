from flask import Blueprint, render_template, session, redirect, url_for, g, request, jsonify
import sqlite3
from chat import get_response

bp = Blueprint('index', __name__)

@bp.route('/')
def home():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, name, price, image_url, description FROM products")
    products = cursor.fetchall()
    cursor.close()
    return render_template('index.html', products=products)

@bp.route('/predict', methods=['POST'])
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)

@bp.route('/product/<int:product_id>')
def view_product(product_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    return render_template('product.html', product=product)

@bp.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    # Retrieve the current cart from the session
    cart = session.get('cart', [])

    # Add the product to the cart
    cart.append(product_id)

    # Update the cart in the session
    session['cart'] = cart

    # Redirect back to the index page
    return redirect(url_for('index.home'))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('products.db')
    return db