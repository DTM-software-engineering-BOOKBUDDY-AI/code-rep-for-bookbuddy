from app import app, db
from models import User, UserPreferences
import random

def test_user_creation():
    with app.app_context():
        try:
            # First, let's see what users exist
            existing_users = User.query.all()
            print("\nExisting users:")
            for user in existing_users:
                print(f"- {user.username} ({user.email})")
            
            # Create a unique username
            random_num = random.randint(1000, 9999)
            test_username = f"testuser{random_num}"
            test_email = f"test{random_num}@example.com"
            
            # Check if username exists
            if User.query.filter_by(username=test_username).first():
                print(f"Username {test_username} already exists!")
                return
                
            # Try to create a test user with unique username
            test_user = User(
                username=test_username,
                email=test_email
            )
            test_user.set_password('password123')
            
            # Create preferences
            test_preferences = UserPreferences(user=test_user)
            
            # Add to database
            db.session.add(test_user)
            db.session.add(test_preferences)
            db.session.commit()
            
            print(f"\nTest user created successfully!")
            print(f"Username: {test_username}")
            print(f"Email: {test_email}")
            
        except Exception as e:
            print(f"Error during test: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    test_user_creation() 