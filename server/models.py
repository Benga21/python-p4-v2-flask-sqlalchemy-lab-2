from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

# Review Model
class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

    # Relationships
    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}, Customer ID: {self.customer_id}, Item ID: {self.item_id}>'

    def to_dict(self, include_customer=True, include_item=True):
        return {
            'id': self.id,
            'comment': self.comment,
            'customer': self.customer.to_dict(include_reviews=False) if include_customer and self.customer else None,
            'item': self.item.to_dict(include_reviews=False) if include_item and self.item else None,
        }


# Customer Model
class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # Relationships
    reviews = db.relationship('Review', back_populates='customer', cascade='all, delete-orphan')
    
    # Association proxy
    items = association_proxy('reviews', 'item', creator=lambda item: Review(item=item))

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

    def to_dict(self, include_reviews=True):
        customer_dict = {
            'id': self.id,
            'name': self.name,
        }
        if include_reviews:
            customer_dict['reviews'] = [review.to_dict(include_customer=False, include_item=False) for review in self.reviews]
        return customer_dict


# Item Model
class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

    # Relationships
    reviews = db.relationship('Review', back_populates='item', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

    def to_dict(self, include_reviews=True):
        item_dict = {
            'id': self.id,
            'name': self.name,
            'price': self.price,
        }
        if include_reviews:
            item_dict['reviews'] = [review.to_dict(include_customer=False, include_item=False) for review in self.reviews]
        return item_dict
