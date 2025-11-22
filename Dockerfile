FROM python:3.10.14-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir requirements.txt

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "8000" ]