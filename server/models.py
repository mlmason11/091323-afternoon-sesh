from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)



class Hero(db.Model):
    __tablename__ = 'heroes'
    serialize_rules = ('-herovillains.hero',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    power = db.Column(db.String)

    herovillains = db.relationship('HeroVillain', back_populates='hero')
    villains = association_proxy('herovillains', 'villain')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'power': self.power,
            'villains': [vi.to_dict() for vi in self.villain]
        }



class Villain(db.Model):
    __tablename__ = 'villains'
    serialize_rules = ('-herovillains.villain',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    secret_lair = db.Column(db.String)

    herovillains = db.relationship('HeroVillain', back_populates='villain')
    heroes = association_proxy('herovillains', 'hero')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'secret_lair': self.secret_lair,
            'heroes': [he.to_dict() for he in self.hero]
        }



class HeroVillain(db.Model):
    __tablename__ = 'herovillains'
    serialize_rules = ('-hero.herovillain', '-villain.herovillain')

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    villain_id = db.Column(db.Integer, db.ForeignKey('villains.id'))

    hero = db.relationship('Hero', back_populates='herovillains')
    villain = db.relationship('Villain', back_populates='herovillains')