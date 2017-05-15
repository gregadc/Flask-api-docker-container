#! /usr/bin/env python
#  -*- coding: utf-8 -*-

"""                                                                                                                                                                          
    Presentation                                                                                                                                                             
    ============                                                                                                                                                             
    Models.                                                                                                                                                                 
                                                                                                                                                                             
"""

import os, sys
from flask import Flask
from flask import Flask, jsonify, abort, make_response, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:123456@catalog_db/gregdb'

db = SQLAlchemy(app)

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    location = db.Column(db.String(120))
    nbr_of_rooms = db.Column(db.Integer)

    def __init__(self, name, location, nbr_of_rooms):
        self.name = name
        self.location = location
        self.nbr_of_rooms = nbr_of_rooms

    def __repr__(self):
        return '<hotel %s' % (self.name)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer)
    standing = db.Column(db.Integer)

    def __init__(self, hotel_id, standing):
        self.hotel_id = hotel_id
        self.standing = standing

    def __repr__(self):
        return '<room %s' % (str(self.name))

class Room_option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    option_name = db.Column(db.String(120))
    option_price = db.Column(db.Integer)

    def __init__(self, option_name, option_price):
        self.option_price = option_price
        self.option_name = option_name

    def __repr__(self):
        return '<room option %s' % (str(self.option_name))

class Room_options_inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    special_price = db.Column(db.Integer)

    def __init__(self, hotel_id, quantity, special_price):
        self.hotel_id = hotel_id
        self.quantity = quantity
        self.special_price = special_price

    def __repr__(self):
        return '<room option %s' % (str(self.id))

class Room_standing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    short_name = db.Column(db.Integer)
    price_base = db.Column(db.Integer)
    max_clients_by_room = db.Column(db.Integer)

    def __init__(self, name, short_name, price_base, max_clients_by_room):
        self.name = hotel_id
        self.short_name = quentity
        self.price_base = special_price
        self.max_clients_by_room = max_clients_by_room

    def __repr__(self):
        return '<room option %s' % (str(self.name))
