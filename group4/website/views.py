from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():

    products = [
        {
            "name": "Item 1",
            "price": 10.00,
            "description": "Description",
            "type": "Item type",
            "reviews": 5,
            "image": "images/placeholder.jpg"
        }
    ]

    return render_template("shop.html", products=products)