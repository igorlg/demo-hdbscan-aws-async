FROM python:3.6

RUN pip install pandas s3fs boto3 requests
RUN mkdir -p /app /tmp/ramdisk
WORKDIR /app

ADD requirements.txt
RUN pip install -r requirements.txt

ADD app.py /app/app.py
ADD utils.py /app/utils.py

CMD ["python", "app.py"]
