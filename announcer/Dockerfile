# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11-slim

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Move files to /app
ADD flaskr /app/flaskr
ADD requirements.txt /app

WORKDIR /app

# Install pip requirements
RUN python -m pip install -r requirements.txt
# Init flask sqlite database
#RUN flask --app flaskr init-db

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser 
RUN chown -R appuser ./*

# Enter appuser
USER appuser

# Fix permissions of files (777 because I'm lazy)
RUN chmod -R 777 ./*

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "flaskr:create_app()"]
#CMD ["flask", "--app", "flaskr:create_app()", "run"]
