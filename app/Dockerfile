FROM python:3.8-slim-bullseye

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

ENV FLASK_APP app.py

CMD ["flask", "run", "--host=0.0.0.0"]