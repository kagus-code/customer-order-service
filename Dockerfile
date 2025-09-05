FROM python:3.12.1

# Create non-root user early
RUN useradd -m app

# set work directory
WORKDIR /customer-order-service

# environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update && \
    apt-get install -y build-essential curl && \
    pip install --upgrade pip && \
    pip install pipenv && \
    rm -rf /var/lib/apt/lists/*

# copy project files
COPY . .

# copy Pipfile and Pipfile.lock
COPY ./Pipfile ./Pipfile.lock /customer-order-service/

# install pipenv packages
RUN python3 -m pipenv install --system --deploy --ignore-pipfile

# create static and media dirs (fixes STATICFILES_DIRS warning)
RUN mkdir -p /customer-order-service/static \
    && mkdir -p /customer-order-service/staticfiles \
    && mkdir -p /customer-order-service/media

# fix permissions for static + media so non-root user can write
RUN chown -R app:app /customer-order-service

# copy entrypoint script and make it executable
COPY entrypoint.sh /customer-order-service/
RUN chmod +x /customer-order-service/entrypoint.sh

# Switch to non-root user
USER app
