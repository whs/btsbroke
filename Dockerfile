FROM python:3.6-stretch
WORKDIR /app/

ARG TINI_VERSION=v0.16.1
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini

COPY . /app/
RUN chmod +x /tini \
	&& useradd -d /app -M -s /bin/false app \
	&& chown -R app /app \
	&& apt-get update \
	&& apt-get install -y gettext libsodium18 \
	&& pip install --no-cache-dir -r requirements.txt \
	&& pip install --no-cache-dir hiredis mysqlclient gunicorn \
	&& python -m compileall -j 2 /app/ \
	&& python manage.py compilemessages \
	&& STATICFILES_STORAGE=static_compress.CompressedManifestStaticFilesStorage python manage.py collectstatic --no-input --link \
	&& apt-get purge -y gettext \
	&& apt-get autoremove -y \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

USER app
ENTRYPOINT ["/tini", "--"]
CMD ["python", "manage.py", "runworker"]
