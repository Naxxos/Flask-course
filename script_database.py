from market.models import db, Item, User


db.drop_all()
db.create_all()


item1 = Item(name='Iphone', price=500,
             barcode=123456123456, description='desc')
item2 = Item(name='OnePlus', price=300,
             barcode=789456123456, description='desc')
db.session.add(item1)
db.session.add(item2)
db.session.commit()
