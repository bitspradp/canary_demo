FROM python:alpine
WORKDIR /
ENV SUCCESS_RATE=80 \
    FLASK_APP=app.py
STOPSIGNAL SIGINT
CMD ["python", "/app.py"]
RUN pip install flask prometheus_client
COPY app.py /app.py
COPY version.py /version.py
