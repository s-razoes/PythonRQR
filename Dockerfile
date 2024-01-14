# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

RUN apt update
RUN apt install redis-server -y

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
COPY templates/ /templates/

# Set the environment variable for Flask
ENV FLASK_APP=flask_app.py

# Expose port 5000 for the Flask app
EXPOSE 8000

# Start the Flask app using Gunicorn
#CMD ["gunicorn", "--timeout", "600", "--bind", "0.0.0.0:8000", "flask_app:app", "--log-level", "info"]
#CMD ["redis-server"]
CMD ["sh","boot.sh"]
