from app import app, db
from models import User, UserPreferences

def test_user_creation():
    with app.app_context():
        try:
            # Try to create a test user
            test_user = User(
                username='testuser',
                email='test@example.com'
            )
            test_user.set_password('password123')
            
            # Create preferences
            test_preferences = UserPreferences(user=test_user)
            
            # Add to database
            db.session.add(test_user)
            db.session.add(test_preferences)
            db.session.commit()
            
            print("Test user created successfully!")
            
            # Verify user exists
            user = User.query.filter_by(username='testuser').first()
            if user:
                print(f"User found in database: {user.username}")
            else:
                print("User not found in database!")
                
        except Exception as e:
            print(f"Error during test: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    test_user_creation() 