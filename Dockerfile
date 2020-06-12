FROM python:3.6

RUN mkdir -p /app
WORKDIR /app

ADD requirements.txt
RUN pip install -r requirements.txt

ADD app.py /app/app.py
ADD algorithm.py /app/algorithm.py
ADD utils.py /app/utils.py

CMD ["python", "app.py"]
