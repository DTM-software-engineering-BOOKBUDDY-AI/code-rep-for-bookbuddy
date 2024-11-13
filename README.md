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

<<<<<<< Updated upstream
=======
# BookBuddy Route Map

## Main Routes
| Route | Template | Purpose | Access |
|-------|----------|---------|---------|
| `/` or `/home` | `homepage.html` | Landing page showcasing app features and welcome message | Public |
| `/form` | `form page/form.html` | Book discovery and preference form | Public |
| `/recommendation` | `recommendation.html` | Shows personalized book recommendations | Public |
| `/my_lib` | `my_lib.html` | Personal library showing current, wanted, and finished books | Login Required |

## Book Routes (`/books/*`)
| Route | Template/Response | Purpose | Access |
|-------|------------------|---------|---------|
| `/books/search` | JSON Response | API endpoint for searching books via Google Books | Public |
| `/books/search/results` | `search_results.html` | Displays book search results (max 20 books) | Public |
| `/books/book/<book_id>` | `book_details.html` | Shows detailed information about a specific book | Public |
| `/books/preview/<book_id>` | `book_preview.html` | Displays book preview if available | Public |

## User Management Routes
| Route | Template | Purpose | Access |
|-------|----------|---------|---------|
| `/profile/<username>` | `view_profile.html` | Shows user profile and reading statistics | Public/Private* |
| `/search_user` | JSON Response | API endpoint for user search functionality | Public |
| `/check_users` | `check_users.html` | Lists all users (debug mode only) | Debug Mode |
| `/test_db` | Text Response | Tests database connection | Debug Mode |

*Private profiles are only visible to the profile owner

## Template Connections
- `base.html`: Contains navigation bar with:
  - Home link
  - Book Discovery link
  - Search bar (connects to `/books/search/results`)

- `homepage.html`: Features section showcasing:
  - Social Reading
  - Goal Tracking
  - Smart Recommendations
  - Virtual Library
  - Reading Analytics
  - Virtual Book Clubs

## Key Features by Page
- **My Library** (`/my_lib`):
  - Current reading list with progress
  - Want to read list
  - Finished books list
  - Reading statistics

- **Book Search** (`/books/search/results`):
  - Search functionality
  - Results display
  - Links to detailed book views

- **Profile** (`/profile/<username>`):
  - User information
  - Reading preferences
  - Privacy settings
  - Reading activity
  
>>>>>>> Stashed changes
