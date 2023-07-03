from flask import Blueprint, render_template, session, g
import sqlite3

bp = Blueprint('cart', __name__)


@bp.route('/cart')
def cart():
    if 'cart' not in session or len(session['cart']) == 0:
        return render_template('cart.html', cart_empty=True)

    db = get_db()
    cursor = db.cursor()
    cart_list = []
    for product_id in session['cart']:
        cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
        product = cursor.fetchone()
        cart_list.append(product)

    cursor.close()

    total_price = round(sum(product[2] for product in cart_list),2)
    return render_template('cart.html', cart=cart_list, total_price=total_price)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('products.db')
    return db