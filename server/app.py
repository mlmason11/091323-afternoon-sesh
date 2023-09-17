#!/usr/bin/env python3
from flask import Flask, request, make_response, jsonify, request, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Hero, Villain, HeroVillain # import your models here!

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.get('/')
def index():
    return "Hello world"

@app.get('/debug')
def debug():
    import ipdb; ipdb.set_trace()
    return 'debugging...'





@app.get('/heroes')
def all_heroes():
    try:
        heroes = Hero.query.all()
        return make_response(jsonify([hero.to_dict() for hero in heroes]), 200)
    except AttributeError:
        return make_response({ 'error': '404 not found' }, 404)

@app.get('/heroes/<int:id>')
def hero_by_id(id:int):
    try:
        hero = Hero.query.filter(Hero.id == id).first()
        return make_response(jsonify(hero.to_dict()), 200)
    except AttributeError:
        return make_response({ 'error': '404 not found' }, 404)

@app.post('/heroes')
def create_hero():
    try:
        hero_data = request.json
        hero = Hero( name=hero_data['name'], power=hero_data['power'] )
        db.session.add( hero )
        db.session.commit()
        return make_response(jsonify(hero.to_dict()), 201)
    except AttributeError:
        return make_response({ 'error': '404 not found' }, 404)

@app.patch('/heroes/<int:id>')
def update_heroes(id):
    try:
        data_to_update = request.json
        Hero.query.where(Hero.id == id).update(data_to_update)
        db.session.commit()
        hero = Hero.query.filter(Hero.id == id).first()
        return make_response(jsonify(hero.to_dict()), 202)
    except AttributeError:
        return make_response({ 'error': '404 not found' }, 404)

@app.delete('/heroes/<int:id>')
def delete_hero(id):
    try:
        hero = Hero.query.filter(Hero.id == id).first()
        db.session.delete(hero)
        db.session.commit()
        return make_response(jsonify({}), 204)
    except:
        return make_response({'error': '404 could not delete - villain id not found'})



@app.get('/villains')
def all_villains():
    try:
        villains = Villain.query.all()
        return make_response(jsonify([villain.to_dict() for villain in villains]), 200)
    except AttributeError:
        return make_response({ 'error': '404 not found' }, 404)

@app.get('/villains/<int:id>')
def villain_by_id(id:int):
    try:
        villain = Villain.query.filter(Villain.id == id).first()
        return make_response(jsonify(villain.to_dict()), 200)
    except AttributeError:
        return make_response({ 'error': '404 not found' }, 404)

@app.post('/villains')
def create_villain():
    try:
        villain_data = request.json
        villain = Villain( name=villain_data['name'], secret_lair=villain_data['secret_lair'] )
        db.session.add( villain )
        db.session.commit()
        return make_response(jsonify(villain.to_dict()), 201)
    except AttributeError:
        return make_response({ 'error': '404 not found' }, 404)

@app.patch('/villains/<int:id>')
def update_villain(id):
    try:
        data_to_update = request.json
        Villain.query.where(Villain.id == id).update(data_to_update)
        db.session.commit()
        villain = Villain.query.filter(Villain.id == id).first()
        return make_response(jsonify(villain.to_dict()), 202)
    except AttributeError:
        return make_response({ 'error': '404 not found' }, 404)

@app.delete('/villains/<int:id>')
def delete_villain(id):
    try:
        villain = Villain.query.filter(Villain.id == id).first()
        db.session.delete(villain)
        db.session.commit()
        return make_response(jsonify({}), 204)
    except:
        return make_response({'error': '404 could not delete - villain id not found'})


if __name__ == '__main__':
    app.run(port=5555, debug=True)
