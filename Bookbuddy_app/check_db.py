from app import app, db
from models import User

def check_database():
    with app.app_context():
        try:
            # Get all users
            users = User.query.all()
            
            if not users:
                print("No users found in database.")
            else:
                print("\nRegistered Users:")
                print("-----------------")
                for user in users:
                    print(f"ID: {user.id}")
                    print(f"Username: {user.username}")
                    print(f"Email: {user.email}")
                    print("-----------------")
                    
        except Exception as e:
            print(f"Error accessing database: {e}")

if __name__ == "__main__":
    check_database() 