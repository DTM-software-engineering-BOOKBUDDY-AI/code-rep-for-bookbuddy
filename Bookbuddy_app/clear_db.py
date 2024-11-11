from app import app, db
from models import User, UserPreferences

def clear_database():
    with app.app_context():
        try:
            # Delete all users and their preferences
            UserPreferences.query.delete()
            User.query.delete()
            db.session.commit()
            print("Database cleared successfully!")
        except Exception as e:
            print(f"Error clearing database: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    clear_database() 