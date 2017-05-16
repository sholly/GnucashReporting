FROM ubuntu:latest
MAINTAINER Jay Shollenberger jay@jayshollenberger.com
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential libmysqlclient-dev vim
COPY src/gnucashreports_settings.cfg /config/
COPY src/requirements.txt /requirements/requirements.txt
WORKDIR /requirements
RUN pip3 install -r requirements.txt
#COPY src /app
#WORKDIR /app
#ENTRYPOINT ["python3"]
#CMD ["flask_app.py"]
