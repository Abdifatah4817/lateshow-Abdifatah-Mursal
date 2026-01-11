#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Episode, Guest, Appearance
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

class Episodes(Resource):
    def get(self):
        episodes = Episode.query.all()
        episodes_list = [{"id": episode.id, "date": episode.date, "number": episode.number} for episode in episodes]
        return make_response(jsonify(episodes_list), 200)

api.add_resource(Episodes, '/episodes')

class EpisodeById(Resource):
    def get(self, id):
        episode = Episode.query.filter_by(id=id).first()
        
        if not episode:
            return make_response(jsonify({"error": "Episode not found"}), 404)
        
        appearances_list = []
        for appearance in episode.appearances:
            appearances_list.append({
                "episode_id": appearance.episode_id,
                "guest": {
                    "id": appearance.guest.id,
                    "name": appearance.guest.name,
                    "occupation": appearance.guest.occupation
                },
                "guest_id": appearance.guest_id,
                "id": appearance.id,
                "rating": appearance.rating
            })
        
        episode_data = {
            "id": episode.id,
            "date": episode.date,
            "number": episode.number,
            "appearances": appearances_list
        }
        
        return make_response(jsonify(episode_data), 200)
    
    def delete(self, id):
        episode = Episode.query.filter_by(id=id).first()
        
        if not episode:
            return make_response(jsonify({"error": "Episode not found"}), 404)
        
        # Delete related appearances first (cascade should handle this, but being explicit)
        Appearance.query.filter_by(episode_id=id).delete()
        db.session.delete(episode)
        db.session.commit()
        
        return make_response('', 204)

api.add_resource(EpisodeById, '/episodes/<int:id>')

class Guests(Resource):
    def get(self):
        guests = Guest.query.all()
        guests_list = [{"id": guest.id, "name": guest.name, "occupation": guest.occupation} for guest in guests]
        return make_response(jsonify(guests_list), 200)

api.add_resource(Guests, '/guests')

class Appearances(Resource):
    def post(self):
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['rating', 'episode_id', 'guest_id']
            for field in required_fields:
                if field not in data:
                    return make_response(jsonify({"errors": [f"{field} is required"]}), 400)
            
            # Check if episode exists
            episode = Episode.query.filter_by(id=data['episode_id']).first()
            if not episode:
                return make_response(jsonify({"errors": ["Episode not found"]}), 404)
            
            # Check if guest exists
            guest = Guest.query.filter_by(id=data['guest_id']).first()
            if not guest:
                return make_response(jsonify({"errors": ["Guest not found"]}), 404)
            
            # Create new appearance
            appearance = Appearance(
                rating=data['rating'],
                episode_id=data['episode_id'],
                guest_id=data['guest_id']
            )
            
            db.session.add(appearance)
            db.session.commit()
            
            # Prepare response
            response_data = {
                "id": appearance.id,
                "rating": appearance.rating,
                "guest_id": appearance.guest_id,
                "episode_id": appearance.episode_id,
                "episode": {
                    "date": episode.date,
                    "id": episode.id,
                    "number": episode.number
                },
                "guest": {
                    "id": guest.id,
                    "name": guest.name,
                    "occupation": guest.occupation
                }
            }
            
            return make_response(jsonify(response_data), 201)
            
        except ValueError as e:
            return make_response(jsonify({"errors": [str(e)]}), 400)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"errors": ["Validation errors"]}), 400)

api.add_resource(Appearances, '/appearances')

@app.route('/')
def index():
    return '<h1>Late Show API</h1>'

if __name__ == '__main__':
    app.run(port=5555, debug=True)