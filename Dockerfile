# Use an official Python runtime as a parent image
FROM tiangolo/uvicorn-gunicorn:python3.8-slim

COPY requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt

COPY . .

# run the main.py file
CMD ["python", "main.py"]
