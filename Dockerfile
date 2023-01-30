FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR testhub_app/
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["gunicorn", "--config", "gunicorn.py", "config.wsgi"]
