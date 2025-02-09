FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir poetry

RUN poetry install --without dev

ENV PYTHONUNBUFFERED=1

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
