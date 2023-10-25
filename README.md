# simple_social_network

## Dependency Installation

To install the project dependencies, follow these steps:

1. Use Python version 3.8.10 to create a virtual environment:

    ```bash
    python3.8.10 -m venv venv
    ```

2. Install the dependencies from the `requirements.txt` file using pip:

    ```bash
    pip install -r requirements.txt
    ```

## Database Configuration

1. Create a `.env` file in the project's root directory and specify the database paths:

    ```plaintext
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=db_name
    DB_USER=db_user
    DB_PASS=db_pass
    ```

## Performing Migrations Using Alembic

To perform database migrations using Alembic, follow these commands:
 

1. Create a migration:

    ```bash
    alembic revision --autogenerate -m "Database creation"
    ```

2. Apply the migration:

    ```bash
    alembic upgrade head
    ```

## Starting the Project

Navigate to the `src` directory:

  ```bash
  cd src
  ```

Launch the project using Uvicorn:

  ```bash
  uvicorn main:app 
  ```
View API documentation:
  ```bash
  http://127.0.0.1:8000/docs
  ```


## Running bot

Navigate to the `bot` directory:

  ```bash
  cd bot
  ```
Launch the bot:

  ```bash
  python bot.py run 
  ```
