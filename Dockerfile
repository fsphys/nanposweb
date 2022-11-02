FROM python:3.10-buster

# Define the maintainer of the image
MAINTAINER Fachschaft-Physik <admins@fachschaft.physik.kit.edu>

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1
# Change poetry path from /root to /opt/poetry
ENV POETRY_HOME=/opt/poetry

# Set the timezone, which is required for correct date validation
RUN ln -sf /usr/share/zoneinfo/Europe/Berlin /etc/localtime

# Port exposed by the docker container
EXPOSE 5000
# Set the port for gunicorn
ENV PORT=5000

# Stop the container on an error
RUN set -e

# Update pip
RUN pip install --upgrade pip

# Update the package list
RUN apt-get update --yes --quiet

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Add user that will be used in the container.
RUN useradd nanpos --home-dir /app

# Set this directory to be owned by the user.
RUN chown nanpos:nanpos /app

# Copy the source code of the project into the container.
COPY --chown=nanpos:nanpos . .

# Create a venv for poetry
RUN python3 -m venv $POETRY_HOME

# Update pip in venv
RUN python3 -m pip install --upgrade pip

# Install poetry
RUN $POETRY_HOME/bin/pip install poetry==1.2.0

# Add poetry to the path
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install project in production mode
RUN poetry install --no-dev

# Start gunicorn serving the site
CMD ["poetry", "run", "gunicorn", "-b", "0.0.0.0:5000", "nanposweb:create_app()"]
