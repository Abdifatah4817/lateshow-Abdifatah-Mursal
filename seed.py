#!/usr/bin/env python3

from app import app
from models import db, Episode, Guest, Appearance

def clear_data():
    """Clear existing data from tables"""
    with app.app_context():
        # Clear data in correct order due to foreign key constraints
        Appearance.query.delete()
        Episode.query.delete()
        Guest.query.delete()
        db.session.commit()

def seed_episodes():
    """Seed episodes data"""
    with app.app_context():
        episodes = [
            Episode(date="1/11/99", number=1),
            Episode(date="1/12/99", number=2),
            Episode(date="1/13/99", number=3),
            Episode(date="1/14/99", number=4),
            Episode(date="1/15/99", number=5),
        ]
        db.session.add_all(episodes)
        db.session.commit()
        print("✅ Episodes seeded!")

def seed_guests():
    """Seed guests data"""
    with app.app_context():
        guests = [
            Guest(name="Michael J. Fox", occupation="actor"),
            Guest(name="Sandra Bernhard", occupation="Comedian"),
            Guest(name="Tracey Ullman", occupation="television actress"),
            Guest(name="John Malkovich", occupation="actor"),
            Guest(name="David Bowie", occupation="musician"),
        ]
        db.session.add_all(guests)
        db.session.commit()
        print("✅ Guests seeded!")

def seed_appearances():
    """Seed appearances data"""
    with app.app_context():
        appearances = [
            Appearance(rating=4, episode_id=1, guest_id=1),
            Appearance(rating=5, episode_id=1, guest_id=2),
            Appearance(rating=3, episode_id=2, guest_id=3),
            Appearance(rating=5, episode_id=2, guest_id=4),
            Appearance(rating=2, episode_id=3, guest_id=5),
            Appearance(rating=4, episode_id=4, guest_id=1),
            Appearance(rating=5, episode_id=5, guest_id=3),
        ]
        db.session.add_all(appearances)
        db.session.commit()
        print("✅ Appearances seeded!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        clear_data()
        seed_episodes()
        seed_guests()
        seed_appearances()
        print("🎉 Database seeding completed!")