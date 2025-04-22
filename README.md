# Indian-Banks-API-Server
Bank API
A FastAPI-based RESTful API for managing bank and branch information, with support for CRUD operations and querying branches by city. The API interacts with a PostgreSQL database, using a bank_branches view to combine data from banks and branches tables.
Table of Contents

Features
Technologies
Prerequisites
Installation
Database Setup
Running the Application
API Endpoints
Testing
Project Structure
Contributing
License

Features

Create, read, update, and delete (CRUD) operations for banks and branches.
Query branches by city and bank ID.
Uses a PostgreSQL database with a bank_branches view to join banks and branches data.
Input validation with Pydantic models.
Asynchronous database operations using the databases library.
Automatic database connection management during application lifecycle.

Technologies

FastAPI: Web framework for building APIs.
PostgreSQL: Relational database for storing bank and branch data.
databases: Asynchronous database access library.
Pydantic: Data validation and settings management.
Uvicorn: ASGI server for running the FastAPI application.
Python 3.8+: Programming language.

Prerequisites

Python 3.8 or higher
PostgreSQL 12 or higher
Git
Postman or another API testing tool (optional, for manual testing)

Installation

Clone the Repository:
git clone link of the repo
cd bank-api


Set Up a Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install fastapi uvicorn databases[postgresql] pydantic asyncpg



Database Setup

Install PostgreSQL:

Follow instructions for your OS: PostgreSQL Downloads.


Create a Database:
CREATE DATABASE banks;


Create Tables and View:Execute the following SQL in your PostgreSQL client (e.g., psql):
-- Create banks table
CREATE TABLE banks (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Create branches table
CREATE TABLE branches (
    ifsc VARCHAR(11) PRIMARY KEY,
    bank_id INTEGER NOT NULL,
    branch VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    FOREIGN KEY (bank_id) REFERENCES banks(id)
);

-- Create bank_branches view
CREATE VIEW bank_branches AS
SELECT 
    b.ifsc,
    b.bank_id,
    k.name AS bank_name,
    b.branch,
    b.address,
    b.city,
    b.district,
    b.state
FROM branches b
JOIN banks k ON b.bank_id = k.id;

Import Data into the Specific Tables using the .csv files in the repo.


Update Database URL:

Open database.py and ensure the DATABASE_URL matches your PostgreSQL credentials:DATABASE_URL = "postgresql+asyncpg://postgres:your_password@localhost:5432/banks"





Running the Application

Start the FastAPI Server:
uvicorn main:app --reload


The API will be available at http://127.0.0.1:8000.

Verify the Application:

Visit http://127.0.0.1:8000/ to see the welcome message:{"message": "Welcome to the Bank API"}





API Endpoints
All endpoints are prefixed with /api/v1.
Banks





Project Structure
bank-api/
├── database.py        # Database configuration and connection
├── main.py           # FastAPI application setup and entry point
├── models.py         # Pydantic models for data validation
├── routes.py         # API routes and endpoint logic
├── README.md         # Project documentation
└── requirements.txt  # Python dependencies (optional)

Contributing

Fork the repository.
Create a feature branch (git checkout -b feature/YourFeature).
Commit your changes (git commit -m "Add YourFeature").
Push to the branch (git push origin feature/YourFeature).
Open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
