from flask import  Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Length, Email, DataRequired
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "aaron"
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://postgres:aaron@localhost/project"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

class LoginForm(FlaskForm):
    username = StringField("USERNAME: ", validators=[InputRequired("This is required!")])
    password = PasswordField("PASSWORD: ", validators=[InputRequired()])

class Register(FlaskForm):
    id = StringField("CASHIER ID: ", validators=[InputRequired()])
    name = StringField("CASHIER NAME: ", validators=[InputRequired()])
    address = StringField("ADDRESS: ", validators=[DataRequired()])
    contact = StringField("CONTACT NUMBER: ", validators=[DataRequired()])
    username = StringField("USERNAME: ", validators=[InputRequired()])
    password = PasswordField("PASSWORD: ", validators=[InputRequired()])
    cpassword = PasswordField("CONFIRM PASSWORD: ", validators=[InputRequired()])

class AddItem(FlaskForm):
    code = StringField("ITEM CODE: ", validators=[InputRequired()])
    name = StringField("ITEM NAME: ", validators=[InputRequired()])
    unit = StringField("UNIT PRICE: ", validators=[DataRequired()])
    mark_up = StringField("MARK UP PERCENTAGE: ", validators=[DataRequired()])
    selling = StringField("SELLING PRICE: ", validators=[InputRequired()])
    stocks = StringField("STOCKS: ", validators=[InputRequired()])

class Purchase(FlaskForm):
    purchase_id = StringField("PURCHASE ID: ", validators=[InputRequired()])
    supplier_id = StringField("SUPPLIER ID: ", validators=[InputRequired()])
    item_code = StringField("ITEM CODE: ", validators=[DataRequired()])
    item_name = StringField("ITEM NAME: ", validators=[DataRequired()])
    number = StringField("NUMBER OF ITEMS RECEIVED: ", validators=[DataRequired()])
    date = StringField("DATE: ", validators=[InputRequired()])

@app.route("/")
def index():
    return render_template("index.html")

def index1():
    return render_template("index1.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    login = LoginForm()

    if login.validate_on_submit():
        user = Cashier.query.filter_by(Username= login.username.data).first()
        print(user)
        if user:
            if user.Password == login.password.data:

                return redirect(url_for("admin"))
            else:
                return"<h1><CENTER>INVALID!<h1>"
        else:
            return"<h1><CENTER>INVALID!<h1>"


    return render_template("login.html", form = login)

@app.route("/register", methods = ['GET', 'POST'])
def register():
    register = Register()

    if register.validate_on_submit():
        id = register.id.data
        name = register.name.data
        address=register.address.data
        contact = register.contact.data
        username = register.username.data
        password = register.password.data

        insert = Cashier(Cashier_ID = id, Cashier_Name = name, Address= address, Contact_Number= contact,  Username = username, Password = password)

        db.session.add(insert)
        db.session.commit()

        return redirect(url_for("admin"))

    return render_template("register.html", form = register)

@app.route("/admin", methods = ['GET', 'POST'])
def admin():
    #admin = admin()
    cashierAccount = Cashier.query.all()
    item= Item.query.all()

    return render_template("admin.html", cashierAccount=cashierAccount, item=item)

@app.route("/addItem", methods = ['GET', 'POST'])
def addItem():
    addItem = AddItem()

    if addItem.validate_on_submit():
        code = addItem.code.data
        name = addItem.name.data
        unit = addItem.unit.data
        mark_up = addItem.mark_up.data
        selling = addItem.selling.data
        stocks = addItem.stocks.data


        insert = Item(Item_Code = code, Item_Name = name, Unit_Cost= unit, Mark_Up_Percentage= mark_up,  Selling_Price = selling, Stocks  = stocks)

        db.session.add(insert)
        db.session.commit()

        return redirect(url_for("admin"))

    return render_template("addItem.html", form = addItem)

@app.route("/purchase", methods = ['GET', 'POST'])
def purchase():
    purchase = Purchase()

    if purchase.validate_on_submit():
        purchase_id = purchase.purchase_id.data
        supplier_id = purchase.supplier_id.data
        item_code = purchase.item_code.data
        number = purchase.number.data
        date = purchase.date.data

        insert = Purchase(Purchase_ID = purchase_id, Supplier_ID = supplier_id, Item_Code= item_code, Number_of_Item_Received= number, Date_of_Purchase =date);
        db.session.add(insert)
        db.session.commit()

        return redirect(url_for("admin"))

    return render_template("purchase.html", form=purchase)

# @app.route("/cashierAccount", methods = ['GET', 'POST'])
# def cashierAccount():
#     #admin = admin()
#     cashierAccount = Cashier.query.all()
#     return render_template("cashierAccount.html", cashierAccount=cashierAccount)

if __name__ == '__main__':
    app.run(debug = True)
