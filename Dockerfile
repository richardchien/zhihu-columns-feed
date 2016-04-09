FROM python:3.5.1

ADD app.py app.py
ADD requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "app.py"]
