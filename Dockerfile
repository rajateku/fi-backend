FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

expose 8000

ENTRYPOINT python app.py

# sudo docker container ps
# sudo docker build -t colleges .
# sudo docker container ls
# docker run -t -p 8000:8000 colleges
