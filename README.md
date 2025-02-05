# Customer Order API

## Description

Customer Order API is a Django DRF-based service that provides order management functionality. The API is documented using Swagger and ReDoc, supports OpenID Connect authentication, and is deployed to a DigitalOcean droplet with CI/CD automation via GitHub Actions.

## Features

- **Django REST Framework**: Provides a robust API implementation.
- **OpenID Connect Authentication**: Uses session authentication with OpenID Connect.
- **Celery Integration**: Asynchronous task processing using RabbitMQ as a message broker.

---

## Setup Guide

### Requirements

- Python 3.12.1
- PostgreSQL as Database
- Pipenv
- RabbitMQ

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/kagus-code/customer-order-service.git
   ```
2. Change directory to the project directory:
   ```sh
   cd customer-order-service
   ```
3. Open the project in VS Code (or your preferred editor).
4. Install dependencies using Pipenv:
   ```sh
   pipenv install
   ```
5. Spawn the virtual environment:
   ```sh
   pipenv shell
   ```
6. Create an environment variables file:
   ```sh
   touch .env
   ```
7. Open the `.env` file and enter your environment variables as follows (ensure no spaces around `=`):
   ```ini
   SECRET_KEY=""
   DATABASE_URL=<PostgreSQL database URL>
   DEBUG=<True/False>
   SETTINGS_FILE=<Path to settings file>

   AUTH0_CLIENT_ID=""
   AUTH0_CLIENT_SECRET=""
   AUTH0_DOMAIN=""
   AUTH0_AUDIENCE=""

   BROKER_URL=<RabbitMQ URL>

   AFRICASTALKING_USERNAME=""
   AFRICASTALKING_API_KEY=""

   SERVER_URL=<e.g., http://127.0.0.1:8000>
   ```
8. Apply database migrations:
   ```sh
   python3 manage.py migrate
   ```
9. Run the application:
   ```sh
   python3 manage.py runserver
   ```

---

## Authentication

The API uses **OpenID Connect (OIDC)** for authentication via **Auth0**. To authenticate:

1. Navigate to the authentication endpoint in your browser:
   ```
   http://127.0.0.1:8000/oidc/authenticate/
   ```
2. You will be redirected to the **Auth0 login window**.
3. Upon successful authentication, you will be redirected to **Swagger UI**.
4. You can now test the API while authenticated through a session.

---

## Message Broker (RabbitMQ & Celery)

Celery requires a message broker to store and process tasks. By default, this project uses **RabbitMQ**.

### Installing RabbitMQ
To install RabbitMQ, run:
```sh
sudo apt-get install rabbitmq-server
```
Check the RabbitMQ server status:
```sh
sudo service rabbitmq-server status
```

### Running Celery
1. Open a new terminal window.
2. Activate the virtual environment:
   ```sh
   pipenv shell
   ```
3. Start the Celery worker:
   ```sh
   celery -A crm worker -l info
   ```
4. To clear all pending Celery tasks:
   ```sh
   celery -A crm purge
   ```
   > This command purges all pending tasks in the Celery queue without executing them.

**Note:** In production, Celery should be run as a background daemon.

---

## Testing & Coverage

To run tests with coverage:
```sh
coverage run -m pytest --disable-warnings
coverage report -m
```

---

## Support and Contact

| Name          | Email                   |
|--------------|-------------------------|
| Eston Kagwima | ekagwima745@gmail.com   |

