FROM ubuntu:latest
MAINTAINER Jay Shollenberger jay@jayshollenberger.com
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential libmysqlclient-dev
COPY src /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["flask_app.py"]