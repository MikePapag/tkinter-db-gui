# API GUI Client

A Python Tkinter GUI application to interact with a Flask backend connected to a MySQL database.  
Supports API key authentication with different access levels (user/admin) and CRUD operations on multiple tables.

## Features

- API key verification with role-based access  
- Dropdown selection for tables and HTTP methods  
- Form inputs dynamically change based on method  
- Connects to REST API backend for database operations  

## Requirements

- Python 3  
- tkinter  
- requests  
- Flask (for backend)  
- MySQL database  

## Usage
1. To set up the database, import the boats_schema.sql into your MySQL instance.
2. Create your .env file as seen in .env.example.
3. Run the Flask backend server.  
4. Launch the Tkinter GUI client.  
5. Enter your API key to unlock functionality.  
6. Use the dropdowns and forms to perform CRUD operations.

## Author

Michael Papageorgiou
