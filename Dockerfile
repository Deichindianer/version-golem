FROM python:3.8-alpine

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /opt/version-golem
COPY src/requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .

# ENTRYPOINT ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
ENTRYPOINT ["python", "app.py"]
