FROM python:3.10-slim

COPY ../requirements.freeze.txt .
RUN pip install -r requirements.freeze.txt \
      --no-cache-dir --progress-bar off

WORKDIR /usr/src/app
COPY . .

CMD ["uvicorn", "producer:app", "--host", "0.0.0.0", "--port", "80"]