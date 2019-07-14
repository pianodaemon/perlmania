FROM ubuntu:bionic
MAINTAINER miriam.physics@gmail.com

# getting last software catalog
RUN apt-get update --fix-missing

# Minimal deb packages required
RUN apt-get install -y --no-install-recommends  \
    python3-wheel python3-setuptools python3-pip python3-dev python3-venv\
    libpq-dev

# Remove downloaded .debs from cache
RUN apt-get clean

WORKDIR /app
COPY ./service /app

RUN pip3 install -r requirements.txt

EXPOSE 80

CMD ["python3", "app.py"]
