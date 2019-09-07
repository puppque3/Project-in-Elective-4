from flask import  Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = "aaron"

class LoginForm(FlaskForm):
    username = StringField("USERNAME: ", validators=[InputRequired("This is required!")])
    password = PasswordField("PASSWORD: ", validators=[InputRequired()])

class Register(FlaskForm):
    id = StringField("CASHIER ID: ", validators=[InputRequired()])
    name = StringField("CASHIER NAME: ", validators=[InputRequired()])
    address = StringField("ADDRESS: ", validators=[DataRequired(), Email()])
    contact = StringField("CONTACT NUMBER: ", validators=[DataRequired(), Email()])
    username = StringField("USERNAME: ", validators=[InputRequired()])
    password = PasswordField("PASSWORD: ", validators=[InputRequired()])
    cpassword = PasswordField("CONFIRM PASSWORD: ", validators=[InputRequired()])


@app.route("/")
def index():
    return render_template("index.html")

def index1():
    return render_template("index1.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    login = LoginForm()


    if login.validate_on_submit():
        user = InsertDatabase.query.filter_by(username= login.username.data).first()
        print(user)
        if user:
            if user.password == login.password.data:

                return"<h3><LEFT> Welcome {}! <br><h1><CENTER>WELCOME TO BSIT 4-1 CLASS!<h1>".format(login.username.data)
            else:
                return"<h1><CENTER>INVALID!<h1>"
        else:
            return"<h1><CENTER>INVALID!<h1>"


    return render_template("login.html", form = login)

@app.route("/register", methods = ['GET', 'POST'])
def register():
    register = Register()

    if register.validate_on_submit():
        username = register.username.data
        name = register.name.data
        email = register.email.data
        password = register.password.data

        insert = InsertDatabase(username = username, name = name, email = email, password = password)

        db.session.add(insert)
        db.session.commit()

        return render_template ("registerS.html")

    return render_template("register.html", form = register)
    
@app.route("/admin", methods = ['GET', 'POST'])
def admin():
    #admin = admin()
    return render_template("admin.html")

if __name__ == '__main__':
    app.run(debug = True)
