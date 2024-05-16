""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json
from flask import jsonify
from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Baking(db.Model):
    __tablename__ = 'bakings'  # table name is plural, class name is singular
    # Define the User schema with "vars" from object
    
    id = db.Column(db.Integer, primary_key=True)
    _recpie = db.Column(db.String(255), unique = False, nullable = False)
    _name = db.Column(db.String(255), unique = True, nullable = False)
    _points = db.Column(db.Integer, unique = False, nullable = True)
    

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, recpie="", name = "", points = 0):   # variables with self prefix become part of the object, 
        self._recpie = recpie
        self._name = name
        self._points = points

    @property
    def recpie(self):
        return self._recpie
    
    # a setter function, allows name to be updated after initial object creation
    @recpie.setter
    def recpie(self, recpie):
        self._recpie = recpie
    
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def points(self):
        return self._points
    
    # a setter function, allows name to be updated after initial object creation
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
            "recpie": self.recpie,
            "name": self.name,
            "points": self.points
        }

    # # CRUD update: updates user name, password, phone
    # # returns self
    # def update(self, name="", uid="", password="", dob='', favoritefood=''):
    #     """only updates values with length"""
    #     if len(name) > 0:
    #         self.name = name
    #     if len(uid) > 0:
    #         self.uid = uid
    #     if len(password) > 0:
    #         self.set_password(password)
    #     if dob:
    #         self.dob = dob
    #     if len(favoritefood) > 0:
    #         self.favoritefood = favoritefood
    #     db.session.commit()
    #     return self

    # CRUD delete: remove self
    # None
    # def delete(self):
    #     db.session.delete(self)
    #     db.session.commit()
    #     return None


"""Database Creation and Testing """


# Builds working data for testing
def initBakings():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        ingredients_list = [
            ["flour", "egg", "sugar", "butter"],
            ["cookie", "cocoa"],
            ["cookie", "frosting"],
            ["cookie", "cinnamon"],
            ["butter", "butter", "flour", "egg"],
            ["butter", "egg", "custard", "flour"],
            ["flour", "glaze", "egg", "sugar"],
            ["flour", "egg", "sugar", "love"],
            ["flour", "flour", "butter", "yeast"],
            ["banana", "bread"],
            ["cocoa", "bread"],
            ["cinnamon", "bread", "glaze"],
            ["pecan", "bread"],
            ["cocoa", "cocoa", "flour", "sugar"],
            ["cocoa", "flour", "sugar", "sugar"],
            ["cocoa", "glaze", "custard", "flour"],
            ["brownie", "cookie"],
            ["flour", "butter", "sugar"],
            ["muffin", "frosting"],
            ["banana", "muffin"],
            ["lemon", "muffin", "glaze"],
            ["banana", "muffin", "frosting"],
            ["lemon", "muffin", "frosting"],
            ["butter", "flour", "egg", "bread"],
            ["apple", "pie"],
            ["pecan", "pie"],
            ["custard", "pie"],
            ["eggs", "milk", "butter"],
            ["sugar", "butter"],
            ["sugar", "milk"]
        ]
        for i in ingredients_list:
            i.sort()

        baked_goods_list = [
            "cookie",
            "chocolate chip cookie",
            "sugar cookies",
            "snickerdoodle",
            "croissant",
            "cream puff",
            "danish",
            "bundt cake",
            "bread",
            "banana bread",
            "chocolate bread",
            "cinnamon roll",
            "nut bread",
            "brownie",
            "chocolate cake",
            "marble cake",
            "brookie",
            "muffin",
            "cupcake",
            "banana muffins",
            "lemon muffin",
            "banana cupcake",
            "lemon cupcakes",
            "pie",
            "apple pie",
            "pecan pie",
            "custard pie",
            "custard",
            "frosting",
            "glaze"
        ]
        points_list = [4, 2, 2, 2, 4, 4, 4, 4, 4, 2, 2, 3, 2, 4, 4, 4, 2, 3, 2, 3, 3, 3, 3, 4, 2, 2, 2, 3, 2, 2]

        # b1 = Baking(recpie=json.dumps(ingredients_list[0]))
        # bakings = [b1]
        bakings = []
        for i in range(len(ingredients_list)):
            temp = Baking(recpie=json.dumps(ingredients_list[i]), name=baked_goods_list[i], points=points_list[i])
            bakings.append(temp)
        """Builds sample user/note(s) data"""
        for baking in bakings:
            # try:
            #     '''add a few 1 to 4 notes per user'''
            #     for num in range(randrange(1, 4)):
            #         note = "#### " + baking.name + " note " + str(num) + ". \n Generated by test data."
            #         baking.posts.append(Post(id=baking.id, note=note, image='ncs_logo.png'))
            #     '''add user/post data to table'''
            baking.create()