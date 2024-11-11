# BookBuddy Website Code Repository

This repository contains the code for the BookBuddy website.

We are using **Flask** for our backend and **SQLAlchemy** for our database.

## Project Overview
BookBuddy is a web application that recommends books to users based on their preferences and reading history. The platform integrates with external APIs like Google Books and leverages AI algorithms to generate personalized book suggestions.

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python)
- **Database**: SQLAlchemy (PostgreSQL, MySQL, or SQLite)
- **API Integration**: Google Books API, Goodreads API
- **AI Recommendation Engine**:  TensorFlow, Scikit-learn

## Setup Instructions
1. Clone the repository:
   ```bash
   [git clone https://github.com/your-repository/bookbuddy.git](https://github.com/DTM-software-engineering-BOOKBUDDY-AI/code-rep-for-bookbuddy.git)

# Database schema
+----------------+       +-------------------+
|     User       |       |  UserPreferences  |
+----------------+       +-------------------+
| id (PK)        |       | id (PK)          |
| email          |       | user_id (FK) ←----┐
| username       |    ┌--→ favorite_genres   |
| password_hash  |    |  | preferred_language|
| created_at     |    |  | reading_goal     |
| profile_picture|    |  | email_notifications
| bio            |    |  +-------------------+
+----------------+    |
        ↑             |  One-to-One
        |             |  Relationship
        |             |
        |             |
+----------------+    |  +----------------+
|  ReadingList   |    |  |     Book      |
+----------------+    |  +----------------+
| id (PK)        |    |  | id (PK)       |
| user_id (FK) ←-┘    |  | title         |
| book_id (FK) ←------┘  | author        |
| status         |       | cover_image    |
| progress       |       | genre          |
| started_at     |       | language       |
| finished_at    |       | publication_year
+----------------+       | summary        |
                        +----------------+

Relationships:
- User ←--→ UserPreferences (One-to-One)
- User ←--→ ReadingList (One-to-Many)
- Book ←--→ ReadingList (One-to-Many)
- User ←--→ Book (Many-to-Many through ReadingList)

Legend:
PK = Primary Key
FK = Foreign Key
←--→ = Relationship direction

## New Features
- User Profile Management
- Database Integration
- Privacy Settings
- Form Validation

## Setup Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. Set up database: `flask db upgrade`
3. Run the application: `flask run`

