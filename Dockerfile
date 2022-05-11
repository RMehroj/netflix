FROM python:3.8

WORKDIR /code

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
