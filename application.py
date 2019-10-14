from flask import  Flask, render_template, redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Length, Email, DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from decimal import Decimal
from models import *

bootstrap = Bootstrap()

app = Flask(__name__)
app.config['SECRET_KEY'] = "aaron"
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://postgres:aaron@localhost/project2"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["BOOTSTRAP_SERVE_LOCAL"] = True
bootstrap.init_app(app)
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

    if is_logged_in():
        user = session["user"]
        user_db = Cashier.query.filter_by(Username=user).first()
        user = user_db.Username
        access_level = user_db.access_level
        cashier_name = user_db.Cashier_Name

        if access_level == 0:
            return redirect(url_for("admin"))
        else:
            return redirect(url_for("cashier"))

    return render_template("index.html")

def index1():
    return render_template("index1.html")


def is_logged_in():
    return session.get("user") is not None

@app.route("/login", methods=['GET', 'POST'])
def login():
    login = LoginForm()

    if is_logged_in():
        user = session["user"]
        user_db = Cashier.query.filter_by(Username=user).first()
        user = user_db.Username
        access_level = user_db.access_level
        cashier_name = user_db.Cashier_Name

        if access_level == 0:
            return redirect(url_for("admin"))
        else:
            return redirect(url_for("cashier"))


    if login.validate_on_submit():
        user = Cashier.query.filter_by(Username= login.username.data).first() #2
        print(user)
        if user:
            if user.Password == login.password.data:

                session["user"] = user.Username
                session["access_level"] = user.access_level
                session["cashier_name"] = user.Cashier_Name
                session["items"] = []

                if user.access_level == 0:
                    return redirect(url_for("admin"))
                else:
                    return redirect(url_for("cashier"))


            else:
                return"<h1><CENTER>INVALID!<h1>"
        else:
            return"<h1><CENTER>INVALID!<h1>"


    return render_template("login.html", form = login)

@app.route("/logout", methods=["GET", "POST"])
def logout():

    if request.method == "GET":
        return redirect(url_for("index"))

    if is_logged_in():
        session.pop("user")
        session.pop("access_level")
        session.pop("cashier_name")

    return redirect(url_for("index"))


@app.route("/register", methods = ['GET', 'POST'])
def register():
    register = Register()

    if is_logged_in():
        user = session["user"]
        user_db = Cashier.query.filter_by(Username=user).first()
        user = user_db.Username
        access_level = user_db.access_level
        cashier_name = user_db.Cashier_Name

        if access_level == 1:
            return redirect(url_for("cashier"))

    if register.validate_on_submit():
        id = register.id.data
        name = register.name.data
        address=register.address.data
        contact = register.contact.data
        username = register.username.data
        password = register.password.data

        insert = Cashier(Cashier_ID = id, Cashier_Name = name, Address= address, Contact_Number= contact,  Username = username, Password = password) #3

        db.session.add(insert)
        db.session.commit()

        return redirect(url_for("admin"))

    return render_template("register.html", form = register)

@app.route("/admin", methods = ['GET', 'POST'])
def admin():
    #admin = admin()

    if is_logged_in():
        user = session["user"]
        user_db = Cashier.query.filter_by(Username=user).first()
        user = user_db.Username
        access_level = user_db.access_level
        cashier_name = user_db.Cashier_Name

        print(access_level)

        if access_level == 1:
            return redirect(url_for("cashier"))
    else:
        return redirect(url_for("index"))

    cashierAccount = Cashier.query.all() #1
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

@app.route("/cashier", methods = ['GET', 'POST'])
def cashier():



    user = None
    cashier_name = None
    items = None
    items_session = None


    if session.get("items"):
        items_session = session["items"]


    if is_logged_in():
        user = session["user"]
        user_db = Cashier.query.filter_by(Username=user).first()
        user = user_db.Username
        access_level = user_db.access_level
        cashier_name = user_db.Cashier_Name


        if access_level == 0:
            return redirect(url_for("admin"))
    else:
        return redirect(url_for("index"))

    items = Item.query.all()

    if request.method == "POST":
        itemC = request.form.get("itemcode")
        itemP = request.form.get("price")
        itemQ = request.form.get("qty")

        print(itemQ)

        if itemC:

            temp_item = Item.query.filter_by(Item_Code=itemC).first()

            if temp_item:

                is_new = True
                counter = 0

                items_session = session["items"]



                for i in items_session:
                    print(i[1])
                    if itemC == i[1]:
                        is_new = False
                        items_session[counter][2] = int(i[2]) + int(itemQ)
                        items_session[counter][4] = items_session[counter][2] * items_session[counter][3] 
                        session["items"] = items_session
                        break
                    counter += 1

                print(is_new)

                if is_new:
                    item_append = []
                    item_append.append(temp_item.Item_Name)
                    item_append.append(itemC)
                    item_append.append(int(itemQ))
                    item_append.append(float(itemP))
                    #item_append.append(temp_item.Selling_Price)
                    item_append.append((int(itemQ) * int(float(itemP))))

                    items_session.append(item_append)

                    session["items"] = items_session



            # items_session = session["items"]
            #
            # if item not in items_session:
            #     items_session.append()

            #
        redirect(url_for("cashier"))

    return render_template("cashierform.html", cashier_name=cashier_name, items=items, items_session=items_session)

if __name__ == '__main__':
    app.run(debug = True)
