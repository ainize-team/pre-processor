# Dockerfile CPU
FROM python

RUN pip install --upgrade pip

RUN pip install num2words \
    waitress \
    Unidecode \
    contractions \
    flask \
    emoji

WORKDIR /app
COPY . .

EXPOSE 80

CMD ["python", "app.py"]