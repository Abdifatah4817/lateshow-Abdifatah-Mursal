from app import app
from models import db

print("Initializing database...")
with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully!")
