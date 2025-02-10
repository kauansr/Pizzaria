# Pizzeria
- A pizza sales website built with Python and PostgreSQL, using **JWT authentication** and **password hashing** for security.

## Technologies Used
- **Python** for backend logic.
- **Flask** as the web framework.
- **PostgreSQL** for the database.
- **JWT (JSON Web Tokens)** for authentication.
- **bcrypt** for password hashing.
- **Pytest** for testing routes.

## How to Use (Windows)

1. Clone the repository and Navigate to the project folder:
    ```bash
    git clone https://github.com/kauansr/Pizzaria.git

    cd pizzaria
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:
    ```bash
    venv\Scripts\activate.bat
    ```

4. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. **Manually create the `.env` file** in the root directory and add the following variables:

    - **DB_USERNAME**: Your database username.
    - **DB_PASSWORD**: Your database password.
    - **DB_NAME**: Your database name.
    - **DB_HOST**: The database host (defaults to `localhost`).
    - **DB_PORT**: The database port (defaults to `5432`).
    - **SECRET_KEY**: The secret key for JWT.
    - **DEBUG**: Set to `True` for development or `False` for production.

6. Navigate to the `app` directory:
    ```bash
    cd app
    ```

7. Run the application:
    ```bash
    python run.py
    ```

## Authentication & Security

- **JWT (JSON Web Tokens)**: Used for user authentication.
- **Password Hashing**: User passwords are securely hashed and never stored in plain text.


### Notes:
- **Never expose the `.env` file** publicly. Add it to `.gitignore`.