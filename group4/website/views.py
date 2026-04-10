# this is going to be where we keep all of the URL's to images
from flask import Blueprint, render_template

views = Blueprint('views', __name__)
@views.route('/')
def home():
    return render_template('home.html')