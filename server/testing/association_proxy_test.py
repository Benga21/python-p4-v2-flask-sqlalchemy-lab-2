from app import app, db
from server.models import Customer, Item, Review


class TestAssociationProxy:
    '''Customer in models.py'''

    def test_has_association_proxy(self):
        '''has association proxy to items'''
        with app.app_context():
            c = Customer(name='Phil')  # Provide a name for the customer
            i = Item(name='Insulated Mug', price=9.99)  # Provide details for the item
            db.session.add_all([c, i])
            db.session.commit()

            r = Review(comment='great!', customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            assert hasattr(c, 'items')
            assert i in c.items  # This should now work
