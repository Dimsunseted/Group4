# this is going to be where we keep all of the URL's to images
from flask import Blueprint, render_template
from website.models import Product

views = Blueprint('views', __name__)


SHOP_PRODUCTS = [
    # Featured (same as home)
    {"id": 1,"image": "bananas.jpg", "title": "Bananas", "description": "Ripe yellow bananas, perfect for snacking, smoothies, or baking.", "price": "$0.69 / lb"},
    {"id": 2,"image": "eggs.jpg", "title": "Large eggs (12 ct)", "description": "Grade A large eggs from local farms—great for breakfast and recipes.", "price": "$4.49"},
    {"id": 3,"image": "apple.jpg", "title": "Gala apples", "description": "Crisp, sweet Gala apples—ideal for lunchboxes, salads, or a fresh crunch.", "price": "$1.99 / lb"},
    {"id": 4,"image": "cream_cheese.jpg", "title": "Cream cheese (8 oz)", "description": "Smooth, spreadable cream cheese—perfect on bagels, in dips, or for baking.", "price": "$3.49"},
    {"id": 5,"image": "sliced_bread.jpg", "title": "Sliced white bread (1 loaf)", "description": "Soft sandwich bread, pre-sliced for toast, lunches, and everyday meals.", "price": "$2.99"},
    {"id": 6,"image": "velveeta_cheese.png", "title": "Velveeta cheese (16 oz)", "description": "Melts smooth for mac and cheese, nachos, and hot dips—classic pantry staple.", "price": "$5.99"},
    # Additional catalogue items
    {"id": 7,"image": "lactose_free_whole_milk.jpg", "title": "Lactose-free whole milk", "description": "Rich whole milk without lactose—great for cereal or baking.", "price": "$4.29 / half gal"},
    {"id": 8,"image": "rasberry.jpg", "title": "Raspberries", "description": "Sweet tart berries—perfect for yogurt, desserts, or snacking.", "price": "$4.99 / 6 oz"},
    {"id": 9,"image": "avocado.png", "title": "Avocados", "description": "Creamy Hass avocados—ideal for toast, salads, and guacamole.", "price": "$1.29 / ea"},
    {"id": 10,"image": "chicken_breast.png", "title": "Chicken breast", "description": "Boneless skinless breast—lean protein for grilling or stir-fry.", "price": "$6.99 / lb"},
    {"id": 11,"image": "brocolli.jpg", "title": "Broccoli", "description": "Fresh broccoli crowns—steam, roast, or add to stir-fries.", "price": "$1.99 / lb"},
    {"id": 12,"image": "passion_fruit.jpg", "title": "Passion fruit", "description": "Tropical passion fruit—juicy and aromatic, perfect for smoothies and desserts.", "price": "$2.99 / lb"},
    {"id": 13,"image": 'lactose_free_whole_milk.jpg', "title": "Lactose-free whole milk", "description": "Rich whole milk without lactose—great for cereal or baking.", "price": "$4.29 / half gal"},
    {"id": 14,"image": 'rasberry.jpg', "title": "Raspberries", "description": "Sweet tart berries—perfect for yogurt, desserts, or snacking.", "price": "$4.99 / 6 oz"},
    {"id": 15,"image": 'avocado.png', "title": "Avocados", "description": "Creamy Hass avocados—ideal for toast, salads, and guacamole.", "price": "$1.29 / ea"},
    {"id": 16,"image": 'chicken_breast.png', "title": "Chicken breast", "description": "Boneless skinless breast—lean protein for grilling or stir-fry.", "price": "$6.99 / lb"},
    {"id": 17,"image": 'brocolli.jpg', "title": "Broccoli", "description": "Fresh broccoli crowns—steam, roast, or add to stir-fries.", "price": "$1.99 / lb"},
    {"id": 18,"image": "turkey_breast.jpg", "title": "Turkey breast", "description": "Lean turkey roast cuts—great for sandwiches and dinners.", "price": "$7.99 / lb"},
    {"id": 19,"image": "Mozzerella_cheese_block.jpg", "title": "Mozzarella block", "description": "Mild melting cheese—slice for caprese or shred for pizza.", "price": "$4.99 / 16 oz"},
    {"id": 20,"image": "sliced_mozzerela.jpg", "title": "Sliced mozzarella", "description": "Pre-sliced for sandwiches, paninis, and quick meals.", "price": "$3.99 / 8 oz"},
    {"id": 21,"image": 'chicken_drumsticks.png', "title": 'Chicken drumsticks', "description": 'Family-friendly cuts—bake, grill, or air-fry.', "price": '$2.99 / lb'},
    {"id": 22,"image": 'chicken_thighs.jpg', "title": 'Chicken thighs', "description": 'Flavorful dark meat—great for curries and sheet-pan dinners.', "price": '$3.49 / lb'},
    {"id": 23,"image": "ground_beef.png", "title": "Ground beef", "description": "Versatile ground beef for tacos, meatballs, and sauces.", "price": "$5.99 / lb"},
    {"id": 24,"image": "shreded_parmesan.jpeg", "title": "Shredded parmesan", "description": "Aged parmesan shreds—finish pasta, salads, and soups.", "price": "$3.99 / 5 oz"},
    {"id": 25,"image": "peaches.jpg", "title": "Peaches", "description": "Sweet summer peaches—eat fresh, bake, or grill.", "price": "$2.99 / lb"},
    {"id": 26,"image": "sharp_cheddar_cheese.jpg", "title": "Sharp cheddar", "description": "Aged sharp cheddar—finish pasta, salads, and soups.", "price": "$3.99 / 5 oz"},
]


@views.route('/')
def home():
    products = SHOP_PRODUCTS[:6]
    return render_template('home.html', products=products)


@views.route('/shop')
def shop():
    return render_template('shop.html', products=SHOP_PRODUCTS)
