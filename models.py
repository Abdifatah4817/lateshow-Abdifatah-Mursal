from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'
    
    serialize_rules = ('-appearances.episode',)
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    number = db.Column(db.Integer)
    
    # Relationships
    appearances = db.relationship('Appearance', back_populates='episode', cascade='all, delete-orphan')
    
    # Association proxy
    guests = association_proxy('appearances', 'guest')

class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'
    
    serialize_rules = ('-appearances.guest',)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    occupation = db.Column(db.String)
    
    # Relationships
    appearances = db.relationship('Appearance', back_populates='guest', cascade='all, delete-orphan')
    
    # Association proxy
    episodes = association_proxy('appearances', 'episode')

class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'
    
    serialize_rules = ('-episode.appearances', '-guest.appearances',)
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'))
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'))
    
    # Relationships
    episode = db.relationship('Episode', back_populates='appearances')
    guest = db.relationship('Guest', back_populates='appearances')
    
    # Validations
    @validates('rating')
    def validate_rating(self, key, rating):
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return rating