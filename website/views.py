# this is going to be where we keep all of the URL's to images
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from website.models import Product, Cart
from . import db

views = Blueprint('views', __name__)


SHOP_PRODUCTS = [
    # Featured (same as home)
    {"image": "bananas.jpg", "title": "Bananas", "description": "Ripe yellow bananas, perfect for snacking, smoothies, or baking.", "price": "$0.69 / lb"},
    {"image": "eggs.jpg", "title": "Large eggs (12 ct)", "description": "Grade A large eggs from local farms—great for breakfast and recipes.", "price": "$4.49"},
    {"image": "apple.jpg", "title": "Gala apples", "description": "Crisp, sweet Gala apples—ideal for lunchboxes, salads, or a fresh crunch.", "price": "$1.99 / lb"},
    {"image": "cream_cheese.jpg", "title": "Cream cheese (8 oz)", "description": "Smooth, spreadable cream cheese—perfect on bagels, in dips, or for baking.", "price": "$3.49"},
    {"image": "sliced_bread.jpg", "title": "Sliced white bread (1 loaf)", "description": "Soft sandwich bread, pre-sliced for toast, lunches, and everyday meals.", "price": "$2.99"},
    {"image": "velveeta_cheese.png", "title": "Velveeta cheese (16 oz)", "description": "Melts smooth for mac and cheese, nachos, and hot dips—classic pantry staple.", "price": "$5.99"},
    # Additional catalogue items
    {"image": "lactose_free_whole_milk.jpg", "title": "Lactose-free whole milk", "description": "Rich whole milk without lactose—great for cereal or baking.", "price": "$4.29 / half gal"},
    {"image": "rasberry.jpg", "title": "Raspberries", "description": "Sweet tart berries—perfect for yogurt, desserts, or snacking.", "price": "$4.99 / 6 oz"},
    {"image": "avocado.png", "title": "Avocados", "description": "Creamy Hass avocados—ideal for toast, salads, and guacamole.", "price": "$1.29 / ea"},
    {"image": "chicken_breast.png", "title": "Chicken breast", "description": "Boneless skinless breast—lean protein for grilling or stir-fry.", "price": "$6.99 / lb"},
    {"image": "brocolli.jpg", "title": "Broccoli", "description": "Fresh broccoli crowns—steam, roast, or add to stir-fries.", "price": "$1.99 / lb"},
    {"image": "passion_fruit.jpg", "title": "Passion fruit", "description": "Tropical tang—scoop the pulp for drinks, desserts, or yogurt.", "price": "$2.49 / lb"},
    {"image": "turkey_thigh.jpeg", "title": "Turkey thighs", "description": "Juicy dark meat—roast or braise for hearty meals.", "price": "$4.49 / lb"},
    {"image": "cabbage.jpg", "title": "Green cabbage", "description": "Crisp cabbage for slaw, soups, or stir-fries.", "price": "$0.99 / lb"},
    {"image": "oranges.jpeg", "title": "Oranges", "description": "Juicy citrus—easy to peel for snacks or fresh juice.", "price": "$1.29 / lb"},
    {"image": "turkey_breast.jpg", "title": "Turkey breast", "description": "Lean turkey roast cuts—great for sandwiches and dinners.", "price": "$7.99 / lb"},
    {"image": "Mozzerella_cheese_block.jpg", "title": "Mozzarella block", "description": "Mild melting cheese—slice for caprese or shred for pizza.", "price": "$4.99 / 16 oz"},
    {"image": "sliced_mozzerela.jpg", "title": "Sliced mozzarella", "description": "Pre-sliced for sandwiches, paninis, and quick meals.", "price": "$3.99 / 8 oz"},
    {"image": "chicken_drumsticks.png", "title": "Chicken drumsticks", "description": "Family-friendly cuts—bake, grill, or air-fry.", "price": "$2.99 / lb"},
    {"image": "chicken_thighs.jpg", "title": "Chicken thighs", "description": "Flavorful dark meat—great for curries and sheet-pan dinners.", "price": "$3.49 / lb"},
    {"image": "ground_beef.png", "title": "Ground beef", "description": "Versatile ground beef for tacos, meatballs, and sauces.", "price": "$5.99 / lb"},
    {"image": "shreded_parmesan.jpeg", "title": "Shredded parmesan", "description": "Aged parmesan shreds—finish pasta, salads, and soups.", "price": "$3.99 / 5 oz"},
    {"image": "peaches.jpg", "title": "Peaches", "description": "Sweet summer peaches—eat fresh, bake, or grill.", "price": "$2.99 / lb"},
    {"image": "sharp_cheddar_cheese.jpg", "title": "Sharp cheddar", "description": "Aged sharp cheddar—finish pasta, salads, and soups.", "price": "$3.99 / 5 oz"},
]


@views.route('/')
def home():
    return render_template('home.html')


@views.route('/shop')
def shop():
    items = Product.query.all()
    return render_template('shop.html', products=items)

@views.route('/shop')
def shop():
    search = request.args.get('search', '').strip()
    sort   = request.args.get('sort', '')
 
    query = Product.query
 
    if search:
        like = f'%{search}%'
        query = query.filter(
            Product.product_name.ilike(like)
        )
 
    if sort == 'price-asc':
        query = query.order_by(Product.current_price.asc())
    elif sort == 'price-desc':
        query = query.order_by(Product.current_price.desc())
    elif sort == 'avail-desc':
        query = query.order_by(Product.in_stock.desc())
    elif sort == 'avail-asc':
        query = query.order_by(Product.in_stock.asc())
 
    products = query.all()
    return render_template('shop.html', products=products, search=search, sort=sort)


@views.route('/add-to-cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
 
    if product.in_stock < 1:
        flash(f'Sorry, {product.product_name} is out of stock.')
        return redirect('shop.html')
 
    cart_item = Cart.query.filter_by(
        customer_link=current_user.id,
        product_link=product_id
    ).first()
 
    if cart_item:
        if cart_item.quantity < product.in_stock:
            cart_item.quantity += 1
            flash(f'Added another {product.product_name} to your cart.')
        else:
            flash(f'You already have the maximum available quantity in your cart.')
    else:
        new_item = Cart(
            quantity=1,
            customer_link=current_user.id,
            product_link=product_id
        )
        db.session.add(new_item)
        flash(f'{product.product_name} added to cart!')
 
    db.session.commit()
    return redirect('shop.html')
 
@views.route('/cart')
@login_required
def cart():
    cart_items = Cart.query.filter_by(customer_link=current_user.id).all()
    subtotal = sum(item.product.current_price * item.quantity for item in cart_items)
    tax      = round(subtotal * 0.0825, 2)
    total    = round(subtotal + tax, 2)
    return render_template('cart.html',
                           cart_items=cart_items,
                           subtotal=round(subtotal, 2),
                           tax=tax,
                           total=total)
 
@views.route('/update-cart/<int:cart_id>/<action>')
@login_required
def update_cart(cart_id, action):
    cart_item = Cart.query.get_or_404(cart_id)
 
    if cart_item.customer_link != current_user.id:
        flash('Unauthorized.')
        return redirect('cart.html')
 
    if action == 'increase':
        if cart_item.quantity < cart_item.product.in_stock:
            cart_item.quantity += 1
        else:
            flash('No more stock available.')
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            db.session.delete(cart_item)
            db.session.commit()
            return redirect('cart.html'))
    elif action == 'remove':
        db.session.delete(cart_item)
        db.session.commit()
        return redirect('cart.html')
 
    db.session.commit()
    return redirect('cart.html')
