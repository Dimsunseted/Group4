from flask import Blueprint, redirect, request, url_for, flash, render_template
from flask_login import current_user, login_required
from .models import Cart, DiscountCode, Order, Product
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

@cart.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():

    cart_items = Cart.query.filter_by(
        customer_link=current_user.id
    ).all()

    subtotal = 0
    for item in cart_items:
        subtotal += item.product.current_price * item.quantity
    subtotal = round(subtotal, 2)
    tax = round(subtotal * 0.0825, 2)

    discount = 0
    discount_code = ""
    if request.method == "POST":
        discount_code = request.form.get("discount_code")

        code = DiscountCode.query.filter_by(code=discount_code, active=True).first()

        if code:
            discount = round(subtotal * (code.percentage / 100), 2)
        else:
            flash("Invalid discount code")

    total = round(subtotal + tax - discount, 2)

    return render_template(
        "checkout.html",
        cart_items=cart_items,
        subtotal=subtotal,
        tax=tax,
        discount=discount,
        total=total,
        discount_code=discount_code
    )

@cart.route('/place-order')
@login_required
def place_order():

    cart_items = Cart.query.filter_by(
        customer_link=current_user.id
    ).all()

    for item in cart_items:
        order = Order(
            quantity=item.quantity,
            price=item.product.current_price * item.quantity,
            status="Pending",
            payment_id="demo",
            customer_link=current_user.id,
            product_link=item.product.id
        )
        db.session.add(order)

    Cart.query.filter_by(customer_link=current_user.id).delete()

    db.session.commit()

    flash("Order placed successfully!")

    return redirect('/')