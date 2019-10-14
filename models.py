from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Item(db.Model):
    __tablename__ = "items"
    Item_Code = db.Column(db.String(21), primary_key=True)
    Item_Name = db.Column(db.String(21), unique=True, nullable=False)
    Unit_Cost = db.Column(db.Float, nullable=False)
    Mark_Up_Percentage = db.Column(db.Float, nullable=False)
    Selling_Price = db.Column(db.Float, nullable=False)
    Stocks = db.Column(db.Integer, nullable=False)
    purchase = db.relationship('Purchase', backref = 'item')
    order = db.relationship('Order', backref = 'item')
    minimum_stock = db.relationship('Minimum_Stock', backref = 'item')

class Purchase(db.Model):
    __tablename__ = "purchases"
    Purchase_ID = db.Column(db.String(21), primary_key=True)
    Supplier_ID = db.Column(db.String(21), db.ForeignKey('suppliers.Supplier_ID'))
    Number_of_Item_Received = db.Column(db.Integer, nullable=False)
    Date_of_Purchase = db.Column(db.DateTime, nullable=False)
    Item_Code = db.Column(db.String(21), db.ForeignKey('items.Item_Code'))

    def __repr__(self):
        return "<item_code %r>" % self.Item_Code

class Order(db.Model):
    __tablename__ = "orders"
    Transaction_Code = db.Column(db.String(21), primary_key=True)
    Order_Date = db.Column(db.DateTime, unique=True, nullable=False)
    Quantity_Bought = db.Column(db.Integer, nullable=False)
    Amount = db.Column(db.Float, nullable=False)
    Total_Amount = db.Column(db.Float, nullable=False)
    Taxable_Amount = db.Column(db.Float, nullable=False)
    Cashier_ID = db.Column(db.Integer, db.ForeignKey('cashiers.id'))
    Item_Code = db.Column(db.String(21), db.ForeignKey('items.Item_Code'))


class Minimum_Stock(db.Model):
    __tablename__ = "minimum_stocks"
    Item_Code = db.Column(db.String(21), db.ForeignKey('items.Item_Code'), primary_key=True)
    max_usage = db.Column(db.Float, nullable=False)
    max_lead_time = db.Column(db.Float, nullable=False)
    average_usage  = db.Column(db.Float, nullable=False)
    average_lead_time = db.Column(db.Float, nullable=False)


class Cashier(db.Model):
    __tablename__ = "cashiers"
    # Cashier_ID = db.Column(db.String(21), primary_key=True)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Cashier_Name = db.Column(db.String(21), nullable=False)
    Address = db.Column(db.String(21), nullable=False)
    Contact_Number= db.Column(db.String(21), nullable=False)
    Username= db.Column(db.String(21), nullable=False)
    Password= db.Column(db.String(21), nullable=False)
    access_level = db.Column(db.Integer, nullable=False)
    orders = db.relationship('Order', backref = 'cashier')

    def __repr__(self):
        return "<username %r>" % self.Username

class Supplier(db.Model):
    __tablename__ = "suppliers"
    Supplier_ID = db.Column(db.String(21), primary_key=True)
    Supplier_Name = db.Column(db.String(21), nullable=False)
    purchase = db.relationship('Purchase', backref = 'supplier')
