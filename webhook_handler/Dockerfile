FROM python:3.12-alpine as base

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

FROM base as deploy

COPY *.py .

CMD ["uvicorn", "webhook_handler:app", "--host", "0.0.0.0", "--port", "80"]