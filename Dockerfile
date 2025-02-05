FROM python:3.12.1

RUN useradd app

# set work directory
WORKDIR /customer-order-service

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update && \
    apt-get install -y build-essential curl && \
    pip install --upgrade pip && \
    pip install pipenv

# copy project files
COPY . .

# copy Pipfile and Pipfile.lock
COPY ./Pipfile /customer-order-service/
COPY ./Pipfile.lock /customer-order-service/

# install pipenv packages
RUN python3 -m pipenv install --system --deploy --ignore-pipfile

# copy entrypoint script and make it executable
COPY entrypoint.sh /customer-order-service/
RUN chmod +x /customer-order-service/entrypoint.sh

# Change ownership to app user
RUN chown -R app:app /customer-order-service

# Switch to app user
USER app
