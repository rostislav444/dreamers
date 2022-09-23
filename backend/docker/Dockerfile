FROM python:3.9.2

# set work directory
WORKDIR ./ecommerce/backend


RUN apt-get update \
    && apt-get -y install gettext libpq-dev gcc libxml2-dev libxmlsec1-dev  \
    build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi \
    libcairo2 libpango-1.0-0 libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 libffi-dev shared-mime-info \
    graphviz \
    && pip install psycopg2



# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV IS_DOCKER Yes

# install dependencies
#RUN pip install --upgrade pip setuptools wheel
COPY ../requirements.txt .
RUN pip install -r requirements.txt


# copy entrypoint.sh
COPY ./docker/entrypoint.sh ./
# RUN sed -i 's/\r$//g' ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

# copy project
COPY .. .



# run entrypoint.sh
# ENTRYPOINT ["./entrypoint.sh"]

