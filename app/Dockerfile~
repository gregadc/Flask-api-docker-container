FROM ubuntu:latest
MAINTAINER Grego "adc.greg@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /API
WORKDIR /API
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["bash", "run_flask.sh"]