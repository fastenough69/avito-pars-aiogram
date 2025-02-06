FROM python:3

COPY . /pyt

WORKDIR /pyt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "/pyt/new_bot/main.py"]
