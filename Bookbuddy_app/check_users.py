from app import app, db
from models import User

# Create an application context
with app.app_context():
    # Query all users
    users = User.query.all()
    
    print("\nRegistered Users:")
    print("-----------------")
    for user in users:
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Created at: {user.created_at}")
        print("-----------------") 