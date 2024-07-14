# Use the official Python image
FROM python:latest

# Set environment variables
ARG HOST
ARG AUTH_PASSWORD
ARG SECRET_KEY
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ENV SECRET_KEY=$SECRET_KEY
ENV AUTH_PASSWORD=$AUTH_PASSWORD
ENV HOST=$HOST
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the rest of the project code into the container
COPY . /app

# Run Django migrations and collect static files
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Expose the port
EXPOSE 8000

# Set the command to run the application
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "backend.wsgi:application"]

# FROM python:latest

# # Set environment variables
# ARG HOST
# ARG AUTH_PASSWORD
# ARG SECRET_KEY
# ARG AWS_ACCESS_KEY_ID
# ARG AWS_SECRET_ACCESS_KEY
# ENV SECRET_KEY=$SECRET_KEY
# ENV AUTH_PASSWORD=$AUTH_PASSWORD
# ENV HOST=$HOST
# ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
# ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Set the working directory in the container
# WORKDIR /app

# # Copy the project code into the container
# COPY . /app

# # Install dependencies
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# # Run Django migrations and collect static files
# RUN python manage.py migrate
# RUN python manage.py collectstatic --noinput

# EXPOSE 8000

# # CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "backend.wsgi:application"]