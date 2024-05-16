""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
class Post(db.Model):
    __tablename__ = 'posts'

    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, unique=False, nullable=False)
    image = db.Column(db.String, unique=False)
    # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Constructor of a Notes object, initializes of instance variables within object
    def __init__(self, id, note, image):
        self.userID = id
        self.note = note
        self.image = image
    # Returns a string representation of the Notes object, similar to java toString()
    # returns string
    def __repr__(self):
        return "Notes(" + str(self.id) + "," + self.note + "," + str(self.userID) + ")"

    # CRUD create, adds a new record to the Notes table
    # returns the object added or None in case of an error
    def create(self):
        try:
            # creates a Notes object from Notes(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Notes table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read, returns dictionary representation of Notes object
    # returns dictionary
    def read(self):
        # encode image
        path = app.config['UPLOAD_FOLDER']
        file = os.path.join(path, self.image)
        file_text = open(file, 'rb')
        file_read = file_text.read()
        file_encode = base64.encodebytes(file_read)
        
        return {
            "id": self.id,
            "userID": self.userID,
            "note": self.note,
            "image": self.image,
            "base64": str(file_encode)
        }


# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class User(db.Model):
    __tablename__ = 'users'  # table name is plural, class name is singular
    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)
    _items = db.Column(db.String(255), unique=False, nullable=False)
    _dob = db.Column(db.Date)
    _favoritefood = db.Column(db.String(255), unique=False, nullable=False)
    _role = db.Column(db.String(20), default="User", nullable=False)
    _points = db.Column(db.Integer, unique=False)
    _friends = db.Column(db.String(20), unique=False, nullable=False)
    _friendrq = db.Column(db.String(255), unique=False, nullable=False)
    _stockmoney = db.Column(db.Integer, unique=False, nullable=False)
    _pfp = db.Column(db.String(255), unique=False, nullable=False)

    
    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    posts = db.relationship("Post", cascade='all, delete', backref='users', lazy=True)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, uid, stockmoney, items="[]", password="123qwerty", dob=date.today(), favoritefood='guac', role="User", points = 0, friends='', friendrq='', pfp=''):
        self._name = name    # variables with self prefix become part of the object, 
        self._uid = uid
        self._friends = friends
        self._stockmoney = stockmoney
        self.friendrq = friendrq
        self.set_password(password)
        self._items = items
        self._dob = dob
        self._favoritefood = favoritefood
        self._role = role
        self._points = points
        self._pfp = pfp

    @property
    def friends(self):
        return self._friends
    
    @friends.setter
    def friends(self, friends):
        self._friends = friends
    
    @property
    def stockmoney(self):
        return self._stockmoney
    
    # a setter function, allows name to be updated after initial object creation
    @stockmoney.setter
    def stockmoney(self, stockmoney):
        self._stockmoney = stockmoney
    @property
    def friendrq(self):
        return self._friendrq
    
    @friendrq.setter
    def friendrq(self, friendrq):
        self._friendrq = friendrq

    # role setter property
    @property
    def role(self):
        return self._role
    
    @role.setter
    def role(self, role):
        self._role = role
    
    @property
    def items(self):
        return self._items

    # inventory of items
    @items.setter
    def items(self, items):
        self._items = items
    
    @property
    def pfp(self):
        return self._pfp

    @pfp.setter
    def pfp(self, pfp):
        self._pfp = pfp

    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    # a getter method, extracts email from object
    @property
    def uid(self):
        return self._uid
    
    # a setter function, allows name to be updated after initial object creation
    @uid.setter
    def uid(self, uid):
        self._uid = uid
        
    # check if uid parameter matches user id in object, return boolean
    def is_uid(self, uid):
        return self._uid == uid
    
    def is_admin(self):
        return self._role == "Admin"
    
    @property
    def password(self):
        return self._password[0:10] + "..." # because of security only show 1st characters

    # update password, this is conventional setter
    def set_password(self, password):
        """Create a hashed password."""
        self._password = generate_password_hash(password, "pbkdf2:sha256", salt_length=10)

    # check password parameter versus stored/encrypted password
    def is_password(self, password):
        """Check against hashed password."""
        result = check_password_hash(self._password, password)
        return result
    
    # dob property is returned as string, to avoid unfriendly outcomes
    @property
    def dob(self):
        dob_string = self._dob.strftime('%m-%d-%Y')
        return dob_string
    
    # dob should be have verification for type date
    @dob.setter
    def dob(self, dob):
        self._dob = dob
    
    @property
    def age(self):
        today = date.today()
        return today.year - self._dob.year - ((today.month, today.day) < (self._dob.month, self._dob.day))

    @property
    def favoritefood(self):
        return self._favoritefood
    
    # a setter function, allows name to be updated after initial object creation
    @favoritefood.setter
    def favoritefood(self, favoritefood):
        self._favoritefood = favoritefood
    @property
    def points(self):
        return self._points
    @points.setter
    def points(self, points):
        self._points = points
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "stockmoney": self.stockmoney,
            "uid": self.uid,
            "friends": self.friends,
            "items": self.items,
            "dob": self.dob,
            "age": self.age,
            "posts": [post.read() for post in self.posts],
            "favoritefood": self.favoritefood,
            "role": self.role,
            "items": self.items,
            "points": self.points,
            "friendrq": self.friendrq,
            "pfp": self.pfp,

        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, uid="", password="", dob='', favoritefood='', stockmoney="", items='', points = 0, pfp=''):
        """only updates values with length"""
        temp = []
        if len(uid) > 0:
            self.uid = uid
        if len(password) > 0:
            self.set_password(password)
        if dob:
            self.dob = dob
        if len(favoritefood) > 0:
            self.favoritefood = favoritefood
        if len(pfp) > 0:
            self.pfp = pfp
        if stockmoney == '':
            self.stockmoney = stockmoney
        if len(items)>0:
            users = User.query.all()
            for user in users:
                print(uid)
                if user.uid == uid:
                    print(user.items, "user.items")
                    temp = json.loads(user.items)
                    print(items)
                    print(temp, "temp0")
                    temp.append(json.loads(items)[-1])
                    print(json.loads(items)[-1], "als;kdfjds")
                    print(temp, "temp")
                    sets = set(temp)
                    temp2 = []
                    for i in sets:
                        temp2.append(i)
                    self.items = json.dumps(temp2)
        self.points = points
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None       
class Stock_Transactions(db.Model):
    __tablename__ = 'stock_transactions'
   
    # define the stock schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _uid = db.Column(db.String(255), unique=False, nullable=False)
    _symbol = db.Column(db.String(255),unique=False,nullable=False)
    _transaction_type = db.Column(db.String(255),unique=False,nullable=False)
    _quantity = db.Column(db.String(255),unique=False,nullable=False)
    _transaction_amount = db.Column(db.Integer, nullable=False)
    # constructor of a User object, initializes the instance variables within object (self)

    def __init__(self,uid,symbol,transaction_type,quantity,transaction_amount):
        self._uid = uid
        self._symbol = symbol
        self._transaction_type = transaction_type
        self._quantity = quantity
        self._transaction_amount = transaction_amount
    
    # uid
    @property
    def uid(self):
        return self._uid
    
    @uid.setter
    def uid(self,uid):
        self._uid = uid
        
    # symbol
    @property
    def symbol(self):
        return self._symbol
    
    @symbol.setter
    def symbol(self,symbol):
        self._symbol = symbol
        
    # transaction type
    @property
    def transaction_type(self):
        return self._transaction_type
    
    @transaction_type.setter
    def transaction_type(self,transaction_type):
        self._transaction_type = transaction_type
        
    #quantity
    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self,quantity):
        self._quantity = quantity
        
    #transaction amount
    @property
    def transaction_amount(self):
        return self._transaction_amount
    
    @transaction_amount.setter
    def transaction_amount(self,transaction_amount):
        self._transaction_amount = transaction_amount
        
        
     # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())
    
    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None
        
    
    # CRUD update: updates user name, password, phone
    # returns self

    def update(self,uid="",symbol="",transaction_type="",quantity="",transaction_amount=""):
        """only updates values with length"""
        if len(uid) > 0:
            self.uid = uid
        if len(symbol) > 0:
            self.symbol = symbol
        if len(transaction_type) > 0:
            self.transaction_type = transaction_type
        if len(quantity) > 0:
            self.quantity = quantity
        if len(transaction_amount) > 0:
            self.transaction_amount = transaction_amount           
        db.session.commit()
        return self
    
    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "symbol": self.symbol,
            "transaction_type": self.transaction_type,
            "quantity": self.quantity,
            "transaction_amount": self.transaction_amount
        }

class Stocks(db.Model):
    _tablename_ = 'stocks'
    
    # define the stock schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _symbol = db.Column(db.String(255),unique=False,nullable=False)
    _company = db.Column(db.String(255),unique=False,nullable=False)
    _quantity = db.Column(db.Integer,unique=False,nullable=False)
    _sheesh = db.Column(db.Integer,unique=False,nullable=False)
    
    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self,symbol,company,quantity,sheesh):
        self._symbol = symbol
        self._company = company
        self._quantity = quantity
        self._sheesh = sheesh
# symbol
    @property
    def symbol(self):
        return self._symbol
    
    @symbol.setter
    def symbol(self,symbol):
        self._symbol = symbol
#company
    @property
    def company(self):
        return self._company
    
    @company.setter
    def company(self,company):
        self._company = company
#quantity
    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self,quantity):
        self._quantity = quantity

#cost
    @property
    def sheesh(self):
        return self._sheesh
    
    @sheesh.setter
    def sheesh(self,sheesh):
        self._sheesh = sheesh
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())
    
    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None
        
     # CRUD update: updates user name, password, phone
    # returns self
    def update(self,symbol="",company="",quantity=None):
        """only updates values with length"""
        if len(symbol) > 0:
            self.symbol = symbol
        #if sheesh > 0:
           # self.sheesh = sheesh
        if len(company) > 0:
            self.company = company
        if quantity is not None:
            self.quantity = quantity
        
        db.session.commit()
        return self
    
    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "symbol": self.symbol,
            "company": self.company,
            "quantity": self.quantity,
            "sheesh": self.sheesh,
        }
"""Database Creation and Testing """


# Builds working data for testing
def initUsers():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        u1 = User(name='FlayFusion', uid='flay',stockmoney=1000, friends=json.dumps(["niko", "lex"]), friendrq=json.dumps(["hop"]), password='123flay', dob=date(1847, 2, 11), role='Admin', items=json.dumps(["egg","flour","sugar","milk","butter"]), points=100)
        u2 = User(name='TheCupcakeChampion', uid='cupcake',stockmoney=1000, friends=json.dumps(["toby", "lex"]), friendrq=json.dumps(["hop"]), password='123cupcake', dob=date(1856, 7, 10), role="User", items=json.dumps(["egg","flour","sugar","milk","butter"]), points=50)
        u3 = User(name='PieProdigy', uid='pie',stockmoney=1000, friends=json.dumps(["niko", "toby"]), friendrq=json.dumps(["hop"]), password='123pie', dob=date(1856, 7, 10), role="User", items=json.dumps(["egg","flour","sugar","milk","butter"]), points=25)
        u4 = User(name='GordonGourmetGrumbles', uid='ramsay',stockmoney=1000, friends=json.dumps(["niko", "lex"]), friendrq=json.dumps(["toby"]), password='123ramsay', dob=date(1906, 12, 9), role="User", items=json.dumps(["egg","flour","sugar","milk","butter"]), points=0)
        users = [u1, u2, u3, u4]

        """Builds sample user/note(s) data"""
        for user in users:
            try:
                '''add a few 1 to 4 notes per user'''
                for num in range(randrange(1, 4)):
                    note = "#### " + user.name + " note " + str(num) + ". \n Generated by test data."
                    user.posts.append(Post(id=user.id, note=note, image='ncs_logo.png'))
                '''add user/post data to table'''
                user.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {user.uid}")