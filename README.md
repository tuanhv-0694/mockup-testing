# Test Project

This is a test project

## Project Structure

```
test-project
├── alembic/
├── src/
│   ├── __init__.py
│   ├── products/
│   │   ├── router.py
│   │   ├── schemas.py
│   ├── orders/
│   │   ├── router.py
│   │   ├── schemas.py
│   ├── reports/
│   │   ├── router.py
│   │   ├── schemas.py
│   ├── config.py
│   ├── models.py
│   ├── database.py
│   └── main.py
├── tests/
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── .env
├── .gitignore
└── alembic.ini
```

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   cd test-project
   ```
2. **Create a virtual environment:**
   ```sh
   python -m venv .venv
   source .venv/bin/activate
   ```
3. **Install the dependencies:**
   ```sh
   pip install -r requirements/base.txt
   ```
4. **Create a `.env` file:**
   ```sh
   cp .env.example .env
   ```
5. **Set up the database:**
   Ensure you have PostgreSQL installed and running. Create a database for the application and update the database connection settings in `src/config.py`.
6. **Run the migrations:**
   ```sh
   alembic upgrade head
   ```
7. **Run the application:**
   ```sh
   uvicorn src.main:app --reload
   ```

## Usage

Once the application is running, you can access the API at `http://127.0.0.1:8000`. You can also access the interactive API documentation at `http://127.0.0.1:8000/docs`.

## Running Tests

To run the unit tests, use the following command:
```sh
pytest tests/
```

## Linting

To check the code for style issues, run:
```sh
flake8 src
```
