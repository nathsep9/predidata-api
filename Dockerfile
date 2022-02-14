# pull official base image
FROM python:3.8.5-alpine

# set work directory
WORKDIR /usr/src/app

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev


# install dependencies
RUN pip install --upgrade pip
RUN python --version
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

# copy project
COPY . .

# run docker-entrypoint.sh
ENTRYPOINT ["sh","./docker-entrypoint.sh"]
