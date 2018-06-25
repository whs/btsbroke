FROM python:3.6-stretch
WORKDIR /app/

ARG TINI_VERSION=v0.16.1
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini

COPY . /app/
RUN chmod +x /tini \
	&& useradd -d /app -M -s /bin/false app \
	&& chown -R app /app \
	&& pip install --no-cache-dir -r requirements.txt \
	&& pip install --no-cache-dir hiredis mysqlclient django_redis gunicorn \
	&& python manage.py collectstatic --no-input --link

USER app
ENTRYPOINT ["/tini", "--"]
CMD ["gunicorn", "-b", "0.0.0.0:8000", "btsbroke.wsgi"]
