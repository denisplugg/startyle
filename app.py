from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from USERSdatabase import Users
from CARDdatabase import Celebrities, Outfits

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databases.db'
app.secret_key = 'fhggk90@#1041,v;gh432!?'
db.init_app(app)


with app.app_context():
    db.create_all()


def add_celebrity(celebrity_name, celebrity_img):
    new_celebrity = Celebrities(celebrity_name=celebrity_name, celebrity_img=celebrity_img)

    try:
        db.session.add(new_celebrity)
        db.session.commit()
    except:
        db.session.rollback()

def add_outfit(name, price, image_url, celebrity_id):
    new_outfit = Outfits(name=name, price=price, image_url=image_url, celebrity_id=celebrity_id)

    try:
        db.session.add(new_outfit)
        db.session.commit()
    except:
        db.session.rollback()      


@app.route("/base")
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/WesternStars")
def Western_Stars():
    return render_template("Western_Stars.html")

@app.route("/RuStreetwear")
def Ru_Streetwear():
    return render_template("Ru_Streetwear.html")

@app.route("/CISStars")
def CIS_Stars():
    return render_template("CIS_Stars.html")

@app.route("/Stars")
def Stars():
    return render_template("Stars.html")
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
    
        hashed_password = generate_password_hash(password)

        user = Users(username=username, email=email, password=hashed_password)

        try:
            db.session.add(user)
            db.session.commit()
            flash('Регистрация успешна! Пожалуйста, войдите.')
            return redirect('/login')
        except:
            db.session.rollback()
            flash('Ошибка регистрации')

    return render_template('register.html')

    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id 
            return redirect('/profile')

        flash('Неверное почта или пароль.')

    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user_id' in session:
        user = Users.query.get(session['user_id'])
        return render_template('profile.html', user=user)
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
