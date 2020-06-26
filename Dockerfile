# Use an official Python runtime as a parent image
FROM python:slim-buster
LABEL maintainer="admin@moe.ph"

# Set environment varibles
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV prod

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
# Install any needed packages specified in requirements.txt
RUN pip install -r /app/requirements.txt

# Copy the current directory contents into the container at /app/
COPY . /app/
# Set the working directory to /app/
WORKDIR /app/

RUN python manage-prod.py makemigrations && python manage-prod.py migrate

RUN useradd wagtail
RUN chown -R wagtail /app
USER wagtail

EXPOSE 8000
CMD exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3
