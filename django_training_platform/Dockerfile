FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /web
ADD . /web
RUN pip install -r requirements.txt


CMD ["/web/manage.py", "makemigrations"]
CMD ["/web/manage.py", "migrate"]

