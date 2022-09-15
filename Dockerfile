FROM python:3-slim

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update && apt-get install -y \
        dumb-init \
	&& pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y gcc \
	&& rm -rf /var/lib/apt/lists/* \
	&& rm -rf /root/.cache/pip

COPY app/ /app/

EXPOSE 8080

ENTRYPOINT [ "dumb-init", "--" ]
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
