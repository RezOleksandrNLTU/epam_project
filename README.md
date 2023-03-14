[![Coverage Status](https://coveralls.io/repos/github/RezOleksandr/epam_final_project/badge.svg)](https://coveralls.io/github/RezOleksandr/epam_final_project)

# E-commerce Platform

## About application

This is simple web application for managing sellers products and orders on an E-commerce platform. With this app user can:

- login as seller or administrator
- view, create, delete or edit information about sellers, products and orders as administrator
- view and edit information about themselves, view, create, delete or edit information about their products and orders as seller
- use search and filters on lists of sellers, products and orders

## How to build

This application requires Python 3.10 or higher and MySQL Server 8.0 or higher installed. This instruction describes how to build this app on Ubuntu Linux using bash.

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/RezOleksandr/epam_final_project.git
   cd epam_final_project
   ```

2. Create virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
    pip install -r requirements.txt
   ```

4. Create database and user for this app:

   ```bash
    mysql -u root -p
    ```
    
    ```sql
    CREATE DATABASE ecom_app;
    CREATE USER 'ecom_app'@'localhost' IDENTIFIED BY 'password';
    GRANT ALL PRIVILEGES ON ecom_app.* TO 'ecom_app'@'localhost';
    FLUSH PRIVILEGES;
    ```
        
5. Set environment variables:

   ```bash
   export FLASK_APP="ecom_app"
   export SQLALCHEMY_DATABASE_URI="mysql+pymysql://ecom_app:password@localhost/ecom_app"
   ```
   
6. Create and run migrations:

   ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```
   
7. Create admin user:

   ```bash
   flask create_admin "name" "email" "phone" "password"
   ```
   
8. Run gunicon server:

   ```bash
    gunicorn --bind 127.0.0.1:5000 wsgi:app


The app should be available on http://127.0.0.1:5000/
   
   
