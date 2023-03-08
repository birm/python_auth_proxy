FROM python:3-stretch

WORKDIR /var/www
COPY ./ ./
RUN pip3 install -r requirements.txt
CMD gunicorn -w 4 -b 0.0.0.0:4000 server:app --timeout 400
