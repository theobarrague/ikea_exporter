FROM docker.io/python:3.14-alpine

RUN adduser -D ikea_exporter
WORKDIR /app
USER ikea_exporter
COPY --chown=ikea_exporter:ikea_exporter . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9850
CMD ["python", "ikea_exporter.py"]
