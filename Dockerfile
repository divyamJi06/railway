#pull the official base image
FROM python:3.10.8

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip 
COPY . /app
RUN pip install -r requirements.txt
RUN python manage.py makemigrations && python manage.py migrate && python manage.py migrate --run-syncdb && python manage.py collectstatic --noinput -c

# copy project
#COPY . /home/divyam/workspace/HFC

EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "project.wsgi:application" ,"--bind","0.0.0.0:8000"]
