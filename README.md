Indian-Banks-API-Server
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
git clone https://github.com/your-username/indian-banks-api-server.git
cd indian-banks-api-server


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


Import Data from CSV Files:

The repository includes banks.csv and branches.csv for populating the tables.
Use the PostgreSQL COPY command or a tool like pgAdmin to import data. Example:\COPY banks(id, name) FROM 'banks.csv' DELIMITER ',' CSV HEADER;
\COPY branches(ifsc, bank_id, branch, address, city, district, state) FROM 'branches.csv' DELIMITER ',' CSV HEADER;


Ensure the CSV files match the table schemas (e.g., banks.csv has id and name columns).


Update Database URL:

Open database.py and ensure the DATABASE_URL matches your PostgreSQL credentials:DATABASE_URL = "postgresql+asyncpg://postgres:your_password@localhost:5432/banks"





Running the Application

Start the FastAPI Server:
uvicorn main:app --host 127.0.0.1 --port 8000 --reload


The API will be available at http://127.0.0.1:8000.
Swagger UI is available at http://127.0.0.1:8000/docs.


Verify the Application:

Visit http://127.0.0.1:8000/ to see the welcome message:{"message": "Welcome to the Bank API"}





API Endpoints
All endpoints are prefixed with /api/v1.
Banks



Method
Endpoint
Description
Request Body
Response



POST
/banks/
Create a new bank
{"id": 171, "name": "HDFC Bank"}
{"id": 171, "name": "HDFC Bank"}


GET
/banks/
List all banks
-
[{"id": 171, "name": "HDFC Bank"}, ...]


GET
/banks/{bank_id}
Get a bank by ID
-
{"id": 171, "name": "HDFC Bank"}


PUT
/banks/{bank_id}
Update a bank
{"id": 171, "name": "HDFC Bank Ltd"}
{"id": 171, "name": "HDFC Bank Ltd"}


DELETE
/banks/{bank_id}
Delete a bank
-
{"detail": "Bank deleted"}


Branches



Method
Endpoint
Description
Request Body
Response



POST
/branches/
Create a new branch
{"ifsc": "AB232431413", "bank_id": 171, "branch": "HB3", "address": "123 Vidharbha Road", "city": "Nagpur", "district": "Vidharbha", "state": "Maharashtra"}
{"ifsc": "AB232431413", "bank_id": 171, "bank_name": "HDFC Bank", ...}


GET
/branches/
List all branches
-
[{"ifsc": "AB232431413", "bank_id": 171, "bank_name": "HDFC Bank", ...}, ...]


GET
/branches/{ifsc}
Get a branch by IFSC
-
{"ifsc": "AB232431413", "bank_id": 171, "bank_name": "HDFC Bank", ...}


PUT
/branches/{ifsc}
Update a branch
{"ifsc": "AB232431413", "bank_id": 171, "branch": "HB3 Updated", ...}
{"ifsc": "AB232431413", "bank_id": 171, "bank_name": "HDFC Bank", ...}


DELETE
/branches/{ifsc}
Delete a branch
-
{"detail": "Branch deleted"}


GET
/branches/city/{city}/{bank_id}
List branches by city and bank ID
-
[{"bank_name": "HDFC Bank", "ifsc": "AB232431413", "branch": "HB3", "city": "Nagpur"}, ...]


Testing

Using Postman:

Create a Bank:

URL: http://127.0.0.1:8000/api/v1/banks/
Method: POST
Headers: Content-Type: application/json
Body:{
    "id": 171,
    "name": "HDFC Bank"
}


Expected Response: 200 OK{
    "id": 171,
    "name": "HDFC Bank"
}




Create a Branch:

URL: http://127.0.0.1:8000/api/v1/branches/
Method: POST
Headers: Content-Type: application/json
Body:{
    "ifsc": "AB232431413",
    "bank_id": 171,
    "branch": "HB3",
    "address": "123 Vidharbha Road",
    "city": "Nagpur",
    "district": "Vidharbha",
    "state": "Maharashtra"
}


Expected Response: 200 OK{
    "ifsc": "AB232431413",
    "bank_id": 171,
    "bank_name": "HDFC Bank",
    "branch": "HB3",
    "address": "123 Vidharbha Road",
    "city": "Nagpur",
    "district": "Vidharbha",
    "state": "Maharashtra"
}




Get Branches by City:

URL: http://127.0.0.1:8000/api/v1/branches/city/Nagpur/171
Method: GET
Expected Response: 200 OK[
    {
        "bank_name": "HDFC Bank",
        "ifsc": "AB232431413",
        "branch": "HB3",
        "city": "Nagpur"
    }
]






Verify View Updates:

The bank_branches view automatically updates when you insert, update, or delete rows in branches or banks, as it’s a JOIN of these tables.
Query directly:SELECT * FROM bank_branches WHERE ifsc = 'AB232431413';





Project Structure
indian-banks-api-server/
├── database.py        # Database configuration and connection
├── main.py           # FastAPI application setup and entry point
├── models.py         # Pydantic models for data validation
├── routes.py         # API routes and endpoint logic
├── banks.csv         # CSV file for banks data
├── branches.csv      # CSV file for branches data
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
