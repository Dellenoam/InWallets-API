# InWallets

The API project for InWallets is a reliable and powerful tool part of the site, developed in accordance with modern RestAPI standards. The main functionality of this API is to check wallet balances on various networks, including BSC, Ethereum, Polygon, Arbitrum and others. Users can easily add multiple EVM wallets using JSON format or by uploading xlsx format files. Next, they can manage these wallets by changing, deleting, and creating groups for them.

And of course, this API also allows users to register on the site with email confirmation, log in and receive JWT tokens, update them, log out, deactivate accounts with email confirmation, and reset passwords via email. The entire authentication and authorization process is carried out using JWT technology, providing a high level of security and convenience for users.

## Technologies Used

Python: "^3.12"

fastAPI: "^0.110.0"

async-click: "^8.1.7.2"

uvicorn: {extras = ["standard"], version = "^0.29.0"}

pydantic-settings: "^2.2.1"

sqlalchemy: {extras = ["asyncio"], version = "^2.0.29"}

alembic: "^1.13.1"

asyncpg: "^0.29.0"

pydantic: {extras = ["email"], version = "^2.6.4"}

pyjwt: {extras = ["crypto"], version = "^2.8.0"}

bcrypt: "^4.1.2"

celery: "^5.3.6"

flower: "^2.0.1"

itsdangerous: "^2.1.2"

openpyxl: "^3.1.2"

python-multipart: "^0.0.9"

web3: "^6.16.0"

## Features

1. User registration with email confirmation
2. Authentication and JWT tokens generation
3. Tokens refreshing
4. Logout
5. Account deactivation with email confirmation
6. Password reset via email
7. Management of multiple EVM wallets
8. Adding wallets using JSON or via Excel file
9. Modifying and deleting wallets
10. Creating wallet groups and organizing wallets within them
11. Retrieving wallet balances across various networks

## How to install

To get started, clone the repository

```bash
git clone https://github.com/Dellenoam/InWallets-API.git
```

Create an .env file and fill in the following configuration parameters using the example below

```plaintext
# DB
DB__URL = "postgresql+asyncpg://username:password@host:port/database_name"

# Cookie
COOKIE__SECURE_FLAG = False | True (choose one)

# Celery
CELERY__BROKER_URL = "amqp://username:password@host:port/celery_vhost"
CELERY__BACKEND = "rpc://"

# Flower
FLOWER__BROKER_API = "http://username:password@host:port/api/"
FLOWER__ADDRESS = YOUR_FLOWER_HOST
FLOWER__PORT = YOUR_FLOWER_PORT

# Email
EMAIL__SMTP_HOST = YOUR_SMTP_HOST
EMAIL__SMTP_PORT = YOUR_SMTP_PORT
EMAIL__SMTP_USER = YOUR_SMTP_USER
EMAIL__SMTP_PASSWORD = YOUR_SMTP_PASSWORD

# Crypto
CRYPTO__SECRET_KEY = YOUR_SECRET_KEY
CRYPTO__SALT_EMAIL_CONFIRMATION = YOUR_SALT_FOR_EMAIL_CONFIRMATION
CRYPTO__SALT_RESET_PASSWORD = YOUR_SALT_FOR_RESET_PASSWORD
CRYPTO__SALT_DEACTIVATE_ACCOUNT = YOUR_SALT_FOR_DEACTIVATE_ACCOUNT
CRYPTO__SALT_REACTIVATE_ACCOUNT = YOUR_SALT_FOR_REACTIVATE_ACCOUNT

# Common
SITE_DOMAIN="host:port"
FRONTEND_DOMAIN="host:port"
```

Create private and public encryption keys

```bash
openssl genrsa -out certs/private.pem 4096
openssl rsa -in certs/private.pem -outform PEM -pubout -out certs/public.pem
```

Create a virtual environment and install poetry. I prefer to use venv and install poetry in the virutal environment rather than the global environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install poetry
```

Install dependencies via poetry

```bash
poetry install --only main
```

Hopefully you have created a database and specified the URL to it in .env, if so apply alembic migration to it.

```bash
alembic upgrade head
```

Now you can try to run the server in development mode via the main.py file

```bash
python manage.py runserver
```

Or you can run it on a specific host or port

```bash
python mange.py runserver --host localhost --port 8000
```

## API Documentation

You can reach API Documentation at /docs or /redoc

## License

This project is licensed under the Apache 2.0 License.
