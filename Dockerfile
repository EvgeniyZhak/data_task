FROM python:3.10

COPY requirements.txt /tmp/requirements.txt

WORKDIR /app

RUN pip install --upgrade pip

RUN pip install -r /tmp/requirements.txt

COPY src /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]