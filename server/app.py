from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate

from models import db, Customer, Item, Review  

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Flask SQLAlchemy Lab 2</h1>'

# Route to show all customers
@app.route('/customers')
def show_customers():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)

# Route to show all items
@app.route('/items')
def show_items():
    items = Item.query.all()
    return render_template('items.html', items=items)

# Add other routes as needed...

if __name__ == '__main__':
    app.run(port=5555, debug=True)
