from database import db

class Celebrities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    celebrity_name = db.Column(db.String(100), nullable=False)
    celebrity_img = db.Column(db.String(200), nullable=False)
    outfits = db.relationship('Outfits', backref='celebrities', lazy=True)

    def __repr__(self):
        return f'<Celebrities {self.celebrity_name}>'

class Outfits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    outfit_item = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    item_img = db.Column(db.String(200), nullable=False)
    celebrity_id = db.Column(db.Integer, db.ForeignKey('celebrities.id'), nullable=False)

    def __repr__(self):
        return f'<Outfits {self.outfit_item}>'
