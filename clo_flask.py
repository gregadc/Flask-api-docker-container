#! /usr/bin/env python
#  -*- coding: utf-8 -*-

"""
    Presentation
    ============
    CLO API.

"""

import json
import os, sys
from raven.contrib.flask import Sentry
from raven import Client
from flask import Flask, jsonify, abort, make_response, request
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from model import app, db, Hotel, Room, Room_option, Room_options_inventory, Room_standing

#client = Client('http://1eed51c408714461a5f3f05c5c3b2bca@0.0.0.0:8080/sentry/clo')
#sentry = Sentry(dsn='http://1eed51c408714461a5f3f05c5c3b2bca:c2acdf70c66a44548eb390ba1f23ecb6@0.0.0.0:8080/sentry/clo')
#sentry.init_app(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run(debug=True, host='0.0.0.0')

reload(sys)
sys.setdefaultencoding('utf8')

@app.route('/', methods=['GET'])
def index():
    try:
        return 'Index page'
    except Exception as error:
        print error

# Hotels methods
@app.route('/hotels/<int:hotel_id>', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'], strict_slashes=False)
@app.route('/hotels/', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'], strict_slashes=False)
def hotels(hotel_id=None):
    try:
        hotels_dict = {}
        if request.method == 'GET':
            if hotel_id:
                hotel_query = Hotel.query.filter_by(id=hotel_id).first()
                hotel_dict = {"id":hotel_query.id, "location":hotel_query.location, "name":hotel_query.name}
                return jsonify(hotel_dict)
            hotels_query = Hotel.query.all()
            hotels_dict['hotels'] = []
            _ = [hotels_dict['hotels'].append({'id':h.id, 'location':h.location, 'name':h.name, 'nbr_of_rooms':h.nbr_of_rooms}) for h in hotels_query ]    
            return jsonify(hotels_dict)
        elif request.method == 'POST':
            if not request.json:
                return 'Bad json or json empty.'
            location = request.json.get('location', '')
            nbr = request.json.get('nbr_of_rooms', 0)
            name = request.json.get('name', '')
            hotel_query = Hotel.query.filter_by(name=name).first()
            if not hotel_query:
                add_hotel = Hotel(name, location, nbr)
                db.session.add(add_hotel)
                db.session.commit()
                return jsonify({'hotel': "OK POST"})
            return jsonify(name+" hotel already exist.")
        elif request.method == "DELETE":
            if not hotel_id: hotel_id = request.json.get('id', 0)
            del_hotel = Hotel.query.filter_by(id=hotel_id).first()
            if del_hotel:
                db.session.delete(del_hotel)
                db.session.commit()
                return jsonify({'hotel': 'DELETED'})
            return jsonify({'hotel': 'hotel id '+str(id_hotel)+' not exist.'})
        elif request.method == "PUT":
            if not request.json or not 'id' in request.json:
                abort(400)
            id_hotel = request.json.get('id', 'null')
            #cu.execute("SELECT * FROM hotels where id == "+id_hotel+";")
            #res_hotels = cu.fetchall()
            if res_hotels:
                name = request.json.get('name', 'null')
                location = request.json.get('location', 'null')
                nbr_of_rooms = request.json.get('nbr_of_rooms', 'null')
                update_hotel = "UPDATE hotels SET SALARY = 15000 WHERE ID = "+str(id_hotel)+";"
                #cu.execute(update_hotel)
                return jsonify({'hotel': "UPDATED"})
            return jsonify({'hotel': 'hotel id '+str(id_hotel)+' not exist.'})
    except:
        abort(404)

# rooms methods
@app.route('/rooms/<int:room_id>', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'], strict_slashes=False)
@app.route('/rooms/', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'], strict_slashes=False)
def get_room(room_id=None):
    try:
        room_dict = {}
        if request.method == 'GET':
            if room_id:
                room_query = Room.query.filter_by(id=room_id).first()
                room_dict = {"hotel_id":room_query.hotel_id, "id":room_query.id, "standing":room_query.standing}
                return jsonify(room_dict)
            rooms_query = Room.query.all()
            room_dict['rooms'] = []
            _ = [room_dict['rooms'].append({'id':r.id, 'hotel_id':r.hotel_id, 'standing':r.standing}) for r in rooms_query ]    
            return jsonify(room_dict)
        elif request.method == 'POST':
            if not request.json:
                return 'Bad json or json empty.'
            hotel_id = request.json.get('hotel_id', 0)
            standing = request.json.get('standing', 0)
            hotel_query = Hotel.query.filter_by(id=hotel_id).first()
            if hotel_query:
                add_room = Room(hotel_id, standing)
                db.session.add(add_room)
                db.session.commit()
                return jsonify({'room': "OK POST"})
            else:
                return jsonify('hotel id '+str(hotel_id)+" not exist for this room.")
            return jsonify({'room': "KO POST"})
        elif request.method == "DELETE":
            if not room_id: 
                room_id = request.json.get('id', 0)
            del_room = Room.query.filter_by(id=room_id).first()
            if del_room:
                db.session.delete(del_room)
                db.session.commit()
                return jsonify({'room': 'DELETED'})
            return jsonify({'room': 'room id '+str(room_id)+' not exist.'})
        elif request.method == "PUT":
            if not request.json or not 'id' in request.json:
                abort(400)
            #cu.execute("SELECT * FROM rooms where id == "+_id+";")
            #res_rooms = cu.fetchall()
            if res_rooms:
                id_hotel = request.json.get('id', '')
                name = request.json.get('name', '')
                location = request.json.get('location', '')
                update_hotel = "UPDATE hotels SET SALARY = 15000 WHERE ID = "+str(id_hotel)+";"
                #cu.execute(update_hotel)
                return jsonify({'hotel': "UPDATED"})
            return jsonify({'hotel': 'hotel id '+str(id_hotel)+' not exist.'})
    except:
        abort(404)

@app.route('/room_options/<int:option_id>', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'], strict_slashes=False)
@app.route('/room_options/', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'], strict_slashes=False)
def get_option(option_id=None):
    try:
        roomOP_dict = {}
        if request.method == 'GET':
            if option_id:
                roomOP_query = Room_option.query.filter_by(id=option_id).first()
                roomOP_dict = {"id":roomOP_query.id, "option_name":roomOP_query.option_name, "option_price": roomOP_query.option_price }
                return jsonify(roomOP_dict)
            roomsOP_query = Room_option.query.all()
            roomOP_dict['roomsOP'] = []
            _ = [roomOP_dict['roomsOP'].append({'id':r.id, 'option_name':r.option_name, 'option_price':r.option_price}) for r in roomsOP_query ]    
            return jsonify(roomOP_dict)
        elif request.method == 'POST':
            if not request.json:
                return 'Bad json or json empty.'
            name = request.json.get('option_name', '')
            price = request.json.get('option_price', 0)
            if name:
                add_roomOP = Room_option(name, price)
                db.session.add(add_roomOP)
                db.session.commit()
                return jsonify({'roomOP': "OK POST"})
            return jsonify({'room': "KO POST"})
        elif request.method == "DELETE":
            if not option_id: 
                option_id = request.json.get('id', 0)
            del_roomOP = Room_option.query.filter_by(id=option_id).first()
            if del_roomOP:
                db.session.delete(del_roomOP)
                db.session.commit()
                return jsonify({'room option': 'DELETED'})
            return jsonify({'room': 'room Option id '+str(option_id)+' not exist.'})
        elif request.method == "PUT":
            print 'terminate PUT'
    except:
        abort(404)

@app.route('/room_standing/<int:room_standing_id>', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'], strict_slashes=False)
@app.route('/room_standing/', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'], strict_slashes=False)
def get_room_standing(room_standing_id=None):
    try:
        roomST_dict = {}
        if request.method == 'GET':
            if room_standing_id:
                roomST_query = Room_standing.query.filter_by(id=room_standing_id).first()
                roomST_dict = {"id":roomST_query.id, "name":roomST_query.name, "price_base": roomST_query.price_base, "max_clients_by_room": roomST_query.max_clients_by_room}
                return jsonify(roomST_dict)
            roomST_query = Room_standing.query.all()
            roomST_dict['standing'] = []
            _ = [roomST_dict['standing'].append({'id':r.id, 'name':r.name, 'price_base':r.price_base, 'max_clients_by_room': r.max_clients_by_room}) for r in roomST_query ]    
            return jsonify(roomST_dict)
        elif request.method == 'POST':
            if not request.json:
                return 'Bad json or json empty.'
            standing_name = request.json.get('standing_name', '')
            standing_shortname = request.json.get('standing_short_name', '')
            price_base = request.json.get('price_base', '')
            max_clients_by_room = request.json.get('max_clients_by_room', '')
            if standing_name:
                add_ST= Room_standing(standing_name, standing_shortname, price_base, max_clients_by_room)
                db.session.add(add_ST)
                db.session.commit()
                return jsonify({'room': "OK POST"})
            return jsonify({'room': "KO POST"})
        elif request.method == "DELETE":   
            if not room_standing_id:
                room_standing_id = request.json.get('id', 0)
            del_roomST = Room_standing.query.filter_by(id=room_standing_id).first()
            if del_roomST:
                db.session.delete(del_roomST)
                db.session.commit()
                return jsonify({'room': 'DELETED'})
            return jsonify({'room': 'room standing id '+str(room_standing_id)+' not exist.'})
        elif request.method == "PUT":
            print 'terminate PUT'
    except:
        abort(404)

@app.route('/room_inventory/<int:room_inventory_id>', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'], strict_slashes=False)
@app.route('/room_inventory/', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'], strict_slashes=False)
def get_room_options_inventory(room_inventory_id=None):
    try:
        roomIN_dict = {}
        if request.method == 'GET':
            if room_inventory_id:
                roomIN_query = Room_options_inventory.query.filter_by(id=room_inventory_id).first()
                roomIN_dict = {"id":roomIN_query.id, "hotel id":roomIN_query.hotel_id,  "special_price":roomIN_query.special_price, "quantity": roomIN_query.quantity}
                return jsonify(roomIN_dict)
            roomIN_query = Room_options_inventory.query.all()
            roomIN_dict['inventory'] = []
            _ = [roomIN_dict['inventory'].append({'id':r.id, 'hotel id':r.hotel_id, 'special_price':r.special_price, 'quantity': r.quantity}) for r in roomIN_query ]    
            return jsonify(roomIN_dict)
        elif request.method == 'POST':
            if not request.json:
                return 'Bad json or json empty.'
            hotel_id = request.json.get('hotel_id', 0)
            special_price = request.json.get('special_price', 0)
            quantity = request.json.get('quantity', 0)
            hotel_query = Hotel.query.filter_by(id=hotel_id).first()
            if hotel_query:
                add_inventory = Room_options_inventory(hotel_id, quantity, special_price)
                db.session.add(add_inventory)
                db.session.commit()
                return jsonify({'room': "OK POST"})
            else:
                return jsonify('hotel id '+str(hotel_id)+" not exist for this room.")
            return jsonify({'room': "KO POST"})
        elif request.method == "DELETE":   
            if not room_inventory_id:
                room_inventory_id = request.json.get('id', 0)
            del_roomIN = Room_options_inventory.query.filter_by(id=room_inventory_id).first()
            if del_roomIN:
                db.session.delete(del_roomIN)
                db.session.commit()
                return jsonify({'room': 'DELETED'})
            return jsonify({'room': 'room inventory id '+str(room_inventory_id)+' not exist.'})
        elif request.method == "PUT":
            print 'terminate PUT'
    except:
        abort(404)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    #db.create_all()
    #app.run(port=5000,debug=True)
    manager.run()
