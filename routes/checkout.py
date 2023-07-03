from flask import Blueprint, render_template, session, request, redirect, url_for

bp = Blueprint('checkout', __name__)

@bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'cart' not in session or len(session['cart']) == 0:
        return redirect(url_for('index.home'))

    if request.method == 'POST':
        # Aqui logica de checkout
        session.pop('cart', None)
        return render_template('checkout.html')

    return render_template('checkout.html')