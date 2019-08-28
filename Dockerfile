FROM python:3.5-slim
WORKDIR /app
RUN useradd -l -r -U django

RUN export DEBIAN_FRONTEND=noninteractive && apt-get update && apt-get install -y build-essential libjpeg-dev libmariadb-dev-compat && apt-get clean
RUN pip install gunicorn
ADD requirements.txt .
RUN pip install -r requirements.txt

ADD climate climate
ADD zivatar zivatar
ADD start.sh .
ADD start0.sh .
ADD manage.py .
RUN mkdir run && chown django run
RUN touch debug.log && chown django debug.log

USER django:django
#EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
#ENV CURRENT_UID=$(id -u):$(id -g)

CMD ["./start.sh"]