# Bank API

A RESTful API built with FastAPI for managing bank and branch data.

## Overview

This project provides a robust API for banking information management, allowing users to create, read, update, and delete bank and branch details. It's built with FastAPI and uses PostgreSQL for data storage.

## Features

- CRUD operations for banks and branches
- Search branches by city and bank ID
- Asynchronous database operations
- Well-documented API endpoints

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs
- [PostgreSQL](https://www.postgresql.org/) - Powerful, open-source relational database
- [asyncpg](https://github.com/MagicStack/asyncpg) - High-performance PostgreSQL client library for Python
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation and settings management

## Installation

### Prerequisites

- Python 3.7+
- PostgreSQL

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/bank-api.git
   cd bank-api
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configure your PostgreSQL connection:
   Update the DATABASE_URL in `database.py` with your credentials:
   ```python
   DATABASE_URL = "postgresql+asyncpg://username:password@localhost:5432/banks"
   ```

4. Create the database schema:
   ```sql
   CREATE TABLE banks (
       id INTEGER PRIMARY KEY,
       name VARCHAR(255) NOT NULL
   );

   CREATE TABLE branches (
       ifsc VARCHAR(11) PRIMARY KEY,
       bank_id INTEGER REFERENCES banks(id),
       branch VARCHAR(255) NOT NULL,
       address TEXT NOT NULL,
       city VARCHAR(255) NOT NULL,
       district VARCHAR(255) NOT NULL,
       state VARCHAR(255) NOT NULL
   );

   CREATE VIEW bank_branches AS
   SELECT b.ifsc, b.bank_id, bk.name as bank_name, b.branch, b.address, b.city, b.district, b.state
   FROM branches b
   JOIN banks bk ON b.bank_id = bk.id;
   ```

5. Import data from CSV files:
   - Prepare your CSV files for banks and branches with appropriate column headers
   - For banks.csv:
     ```bash
     psql -U postgres -d banks -c "\COPY banks(id, name) FROM '/path/to/banks.csv' DELIMITER ',' CSV HEADER;"
     ```
   - For branches.csv:
     ```bash
     psql -U postgres -d banks -c "\COPY branches(ifsc, bank_id, branch, address, city, district, state) FROM '/path/to/branches.csv' DELIMITER ',' CSV HEADER;"
     ```
   - Alternatively, you can use Python to import the data:
     ```python
     import pandas as pd
     import psycopg2

     # Connect to your database
     conn = psycopg2.connect("dbname=banks user=postgres password=yourpassword")
     cursor = conn.cursor()

     # Import banks data
     banks_df = pd.read_csv('banks.csv')
     for _, row in banks_df.iterrows():
         cursor.execute("INSERT INTO banks (id, name) VALUES (%s, %s)",
                       (row['id'], row['name']))

     # Import branches data
     branches_df = pd.read_csv('branches.csv')
     for _, row in branches_df.iterrows():
         cursor.execute("INSERT INTO branches (ifsc, bank_id, branch, address, city, district, state) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (row['ifsc'], row['bank_id'], row['branch'], row['address'], row['city'], row['district'], row['state']))

     # Commit changes and close connection
     conn.commit()
     conn.close()
     ```

6. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

### Banks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/banks/` | Get all banks |
| GET | `/api/v1/banks/{bank_id}` | Get a specific bank by ID |
| POST | `/api/v1/banks/` | Create a new bank |
| PUT | `/api/v1/banks/{bank_id}` | Update a bank |
| DELETE | `/api/v1/banks/{bank_id}` | Delete a bank |

### Branches

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/branches/` | Get all branches |
| GET | `/api/v1/branches/{ifsc}` | Get a specific branch by IFSC code |
| POST | `/api/v1/branches/` | Create a new branch |
| PUT | `/api/v1/branches/{ifsc}` | Update a branch |
| DELETE | `/api/v1/branches/{ifsc}` | Delete a branch |
| GET | `/api/v1/branches/city/{city}/{bank_id}` | Get branches by city and bank ID |

## API Documentation

When the server is running, you can access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Request/Response Examples

### Create a Bank

Request:
```http
POST /api/v1/banks/
Content-Type: application/json

{
  "id": 1,
  "name": "State Bank of India"
}
```

Response:
```json
{
  "id": 1,
  "name": "State Bank of India"
}
```

### Create a Branch

Request:
```http
POST /api/v1/branches/
Content-Type: application/json

{
  "ifsc": "SBIN0001234",
  "bank_id": 1,
  "branch": "Main Branch",
  "address": "123 Main St",
  "city": "Mumbai",
  "district": "Mumbai",
  "state": "Maharashtra"
}
```

Response:
```json
{
  "bank_name": "State Bank of India",
  "ifsc": "SBIN0001234",
  "branch": "Main Branch",
  "address": "123 Main St",
  "city": "Mumbai",
  "district": "Mumbai",
  "state": "Maharashtra"
}
```

### Get Branches by City and Bank ID

Request:
```http
GET /api/v1/branches/city/Mumbai/1
```

Response:
```json
[
  {
    "bank_name": "State Bank of India",
    "ifsc": "SBIN0001234",
    "branch": "Main Branch",
    "city": "Mumbai"
  }
]
```

## Error Handling

The API returns appropriate HTTP status codes:

- 200 OK: Successful request
- 400 Bad Request: Invalid input or business rule violation
- 404 Not Found: Resource not found
- 500 Internal Server Error: Server-side issue

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.