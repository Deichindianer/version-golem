FROM python:3.8-alpine

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /opt/version-golem
COPY src/requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .

ENTRYPOINT ["python", "alert_manager.py"]
