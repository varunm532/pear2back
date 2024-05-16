from __init__ import db, app

class Painting(db.Model):
    userID = db.Column(db.Integer,db.ForeignKey('users.id'))
    id = db.Column(db.Integer,primary_key=True)
    image = db.Column(db.Text)
    
def initImageTable():
    with app.app_context():
        db.create_all()
    