FROM python:latest

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY storage_load.py .

CMD ["python3", "storage_load.py"]