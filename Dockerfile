FROM python:3.10-buster

# Define the maintainer of the image
MAINTAINER Fachschaft-Physik <admins@fachschaft.physik.kit.edu>

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1
# Set Bootstrap and Fontawesome version
ENV BOOTSTRAP_VERSION=5.2.2
ENV FONTAWESOME_VERSION=6.2.0

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

# Copy the requirements.txt to the main folder of the container
COPY requirements.txt /

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Add user that will be used in the container.
RUN useradd nanpos --home-dir /app

# Set this directory to be owned by the user.
RUN chown nanpos:nanpos /app

# Copy the source code of the project into the container.
COPY --chown=nanpos:nanpos . .

# Update the package list, install wget
RUN apt-get update --yes --quiet \
    && apt-get install --yes --quiet --no-install-recommends wget unzip \
    && pip install -r /requirements.txt \
    && pip install "gunicorn" \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir nanposweb/static/css \
    && mkdir nanposweb/static/js

RUN wget -q https://github.com/twbs/bootstrap/releases/download/v${BOOTSTRAP_VERSION}/bootstrap-${BOOTSTRAP_VERSION}-dist.zip -O bootstrap.zip \
    && mkdir bootstrap \
    && unzip -q bootstrap.zip -d bootstrap \
    && cp bootstrap/bootstrap-${BOOTSTRAP_VERSION}-dist/css/bootstrap.min.css nanposweb/static/css/bootstrap.min.css \
    && cp bootstrap/bootstrap-${BOOTSTRAP_VERSION}-dist/js/bootstrap.bundle.min.js nanposweb/static/js/bootstrap.bundle.min.js \
    && rm -f bootstrap.zip \
    && rm -rf bootstrap

RUN mkdir fontawesome \
    && wget -q https://use.fontawesome.com/releases/v${FONTAWESOME_VERSION}/fontawesome-free-${FONTAWESOME_VERSION}-web.zip -O fontawesome.zip \
    && unzip -q fontawesome.zip -d fontawesome \
    && cp fontawesome/fontawesome-free-${FONTAWESOME_VERSION}-web/css/all.min.css nanposweb/static/css/all.min.css \
    && cp fontawesome/fontawesome-free-${FONTAWESOME_VERSION}-web/js/all.min.js nanposweb/static/js/all.min.js \
    && cp -r fontawesome/fontawesome-free-${FONTAWESOME_VERSION}-web/webfonts/ nanposweb/static/webfonts/ \
    && rm -r fontawesome.zip \
    && rm -rf fontawesome

# Update pip in venv
RUN python3 -m pip install --upgrade pip

# Start gunicorn serving the site
CMD ["gunicorn", "-b", "0.0.0.0:5000", "nanposweb:create_app()"]
