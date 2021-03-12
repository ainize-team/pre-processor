# Dockerfile CPU
FROM python

RUN pip install --upgrade pip

RUN pip install num2words \
    waitress \
    Unidecode \
    contractions \
    flask \
    emoji

RUN pip install -U pip setuptools wheel

WORKDIR /app
COPY . .

EXPOSE 80

CMD ["python", "app.py"]