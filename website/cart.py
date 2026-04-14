from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import current_user, login_required
from .models import Cart, Product
from . import db
cart = Blueprint('cart', __name__)

@cart.route('/add-to-cart/<int:product_id>')
@login_required
def add_to_cart(product_id):

    product = Product.query.get(product_id)

    if not product:
        flash("Product does not exist")
        return redirect(url_for('views.shop'))

    item = Cart.query.filter_by(
        customer_link=current_user.id,
        product_link=product_id
    ).first()

    if item:
        item.quantity += 1
    else:
        new_item = Cart(
            quantity=1,
            customer_link=current_user.id,
            product_link=product_id
        )
        db.session.add(new_item)

    db.session.commit()
    flash("Item added to cart")

    return redirect(url_for('views.shop'))


@cart.route('/cart')
@login_required
def view_cart():

    cart_items = Cart.query.filter_by(
        customer_link=current_user.id
    ).all()

    total_price = 0
    for item in cart_items:
        total_price += item.product.current_price * item.quantity

    return render_template(
        'cart.html',
        cart_items=cart_items,
        total_price=total_price
    )

@cart.route('/remove-from-cart/<int:item_id>')
@login_required
def remove_from_cart(item_id):

    item = Cart.query.get(item_id)

    if item and item.customer_link == current_user.id:
        db.session.delete(item)
        db.session.commit()

    return redirect(url_for('cart.view_cart'))

@cart.route('/checkout')
@login_required
def checkout():
    return "<h1>Checkout coming soon</h1>"