from app import app, db
from models import User
from sqlalchemy import inspect

def test_database():
    with app.app_context():
        # Get inspector
        inspector = inspect(db.engine)
        
        # Check if tables exist
        tables = inspector.get_table_names()
        print("Database tables:", tables)
        
        # Check User table structure
        if 'user' in tables:
            columns = inspector.get_columns('user')
            print("\nUser table columns:")
            for column in columns:
                print(f"- {column['name']}: {column['type']}")
        else:
            print("\nUser table not found!")

if __name__ == "__main__":
    test_database() 