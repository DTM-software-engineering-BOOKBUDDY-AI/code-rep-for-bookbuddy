from app import app, db
from models import User, UserPreferences
from sqlalchemy import inspect
import os

def check_database_status():
    with app.app_context():
        inspector = inspect(db.engine)
        
        print("\n=== Database Status Check ===")
        
        # 1. Check if database file exists
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        print(f"\n1. Database file status:")
        print(f"Path: {db_path}")
        print(f"Exists: {os.path.exists(db_path)}")
        
        # 2. List all tables
        tables = inspector.get_table_names()
        print(f"\n2. Tables in database:")
        for table in tables:
            print(f"- {table}")
        
        # 3. Check User table structure
        if 'user' in tables:
            print(f"\n3. User table columns:")
            columns = inspector.get_columns('user')
            for column in columns:
                print(f"- {column['name']}: {column['type']}")
        
        # 4. Count records
        try:
            user_count = User.query.count()
            print(f"\n4. Record counts:")
            print(f"- Users: {user_count}")
        except Exception as e:
            print(f"\nError counting records: {str(e)}")
        
        # 5. Test creating a user
        print("\n5. Testing user creation:")
        try:
            # Only create test user if none exist
            if User.query.count() == 0:
                test_user = User(
                    username="test_user",
                    email="test@example.com",
                    gender="prefer_not_to_say",
                    birthday="2000-01-01"
                )
                test_user.set_password("password123")
                db.session.add(test_user)
                db.session.commit()
                print("- Test user created successfully")
            else:
                print("- Skipped test user creation (users already exist)")
        except Exception as e:
            print(f"- Error creating test user: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    check_database_status() 