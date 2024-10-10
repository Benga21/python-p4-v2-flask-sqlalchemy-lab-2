from app import app, db
from server.models import Customer, Item, Review

class TestReview:
    '''Review model in models.py'''

    def test_can_be_instantiated(self):
        '''can be invoked to create a Python object.'''
        r = Review()
        assert r
        assert isinstance(r, Review)

    def test_has_comment(self):
        '''can be instantiated with a comment attribute.'''
        r = Review(comment='great product!')
        assert r.comment == 'great product!'

    def test_can_be_saved_to_database(self):
        '''can be added to a transaction and committed to review table with comment column.'''
        with app.app_context():
            assert 'comment' in Review.__table__.columns

            # Create and save a Customer and Item instance
            customer = Customer(name='John Doe')
            item = Item(name='Sample Item', price=10.99)
            db.session.add_all([customer, item])
            db.session.commit()  # Commit to get IDs

            # Now create a Review linked to the customer and item
            r = Review(comment='great!', customer_id=customer.id, item_id=item.id)
            db.session.add(r)
            db.session.commit()

            assert hasattr(r, 'id')
            assert db.session.query(Review).filter_by(id=r.id).first()

    def test_is_related_to_customer_and_item(self):
        '''has foreign keys and relationships'''
        with app.app_context():
            assert 'customer_id' in Review.__table__.columns
            assert 'item_id' in Review.__table__.columns

            # Create Customer and Item instances
            customer = Customer(name='Jane Doe')
            item = Item(name='Sample Item', price=9.99)
            db.session.add_all([customer, item])
            db.session.commit()

            # Create a Review linked to the customer and item
            r = Review(comment='great!', customer=customer, item=item)
            db.session.add(r)
            db.session.commit()

            # Check foreign keys
            assert r.customer_id == customer.id
            assert r.item_id == item.id
            # Check relationships
            assert r.customer == customer
            assert r.item == item
            assert r in customer.reviews
            assert r in item.reviews
