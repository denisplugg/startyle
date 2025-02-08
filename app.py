from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from USERSdatabase import Users
from CARDdatabase import ForeignCelebrities, ForeignOutfits, CISCelebrities, CISOutfits, RuBrands, RuOutfits

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databases.db'
app.secret_key = 'fhggk90@#1041,v;gh432!?'
db.init_app(app)


with app.app_context():
    db.create_all()


def add_foreign_celebrity(celebrity_name, celebrity_img, unique_id):
    
    new_foreign_celebrity = ForeignCelebrities(celebrity_name=celebrity_name, celebrity_img=celebrity_img, unique_id=unique_id)

    try:
        db.session.add(new_foreign_celebrity)
        db.session.commit()
        print(f'Foreign Celebrity {celebrity_name} added successfully.')
    except Exception as e:
        db.session.rollback()
        print(f'Error adding foreign celebrity: {str(e)}') 


def add_foreign_outfit(outfit_item, price, item_img, celebrity_id):
    new_foreign_outfit = ForeignOutfits(outfit_item=outfit_item, price=price, item_img=item_img, celebrity_id=celebrity_id)

    try:
        db.session.add(new_foreign_outfit)
        db.session.commit()
    except Exception as e:
        db.session.rollback()  
        print(f'Error adding foreign outfit: {str(e)}') 


def add_cis_celebrity(celebrity_name, celebrity_img):
    new_cis_celebrity = CISCelebrities(celebrity_name=celebrity_name, celebrity_img=celebrity_img)

    try:
        db.session.add(new_cis_celebrity)
        db.session.commit()
        print(f'CIS Celebrity {celebrity_name} added successfully.')
    except Exception as e:
        db.session.rollback()
        print(f'Error adding cis celebrity: {str(e)}') 


def add_cis_outfit(outfit_item, price, item_img, celebrity_id):
    new_cis_outfit = CISOutfits(outfit_item=outfit_item, price=price, item_img=item_img, celebrity_id=celebrity_id)

    try:
        db.session.add(new_cis_outfit)
        db.session.commit()
        print(f'CIS Outfit {outfit_item} added successfully.')
    except Exception as e:
        db.session.rollback()
        print(f'Error adding cis outfit: {str(e)}')


def add_ru_brand(brand_name, brand_logo):
    new_ru_brand = RuBrands(brand_name=brand_name, brand_logo=brand_logo)

    try:
        db.session.add(new_ru_brand)
        db.session.commit()
        print(f'RU Brand {brand_name} added successfully.')
    except Exception as e:
        db.session.rollback()
        print(f'Error adding ru brand: {str(e)}')

def add_ru_outfit(outfit_item, price, item_img, brand_id):
    new_ru_outfit = RuOutfits(outfit_item=outfit_item, price=price, item_img=item_img, brand_id=brand_id)

    try:
        db.session.add(new_ru_outfit)
        db.session.commit()
        print(f'RU Outfit {outfit_item} added successfully.')
    except Exception as e:
        db.session.rollback()
        print(f'Error adding ru outfit: {str(e)}')


@app.route("/base")
@app.route("/", methods=['GET'])
def index():
    fcelebrities = ForeignCelebrities.query.all()
    foutfits = ForeignOutfits.query.all()

    search_query = request.args.get('query', '')
    if search_query:
        fcelebrities = ForeignCelebrities.query.filter(ForeignCelebrities.celebrity_name.ilike(f'%{search_query}%')).all()
    return render_template('index.html', fcelebrities=fcelebrities, foutfits=foutfits, search_query=search_query)

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
        except Exception as e:
            db.session.rollback()
            flash('Ошибка регистрации: {}'.format(str(e)))

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