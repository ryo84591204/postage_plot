FROM python:3.11
COPY requirements.txt .
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

COPY ./src ${VOLUMES:-/app/src}
WORKDIR ${WORK_DIR:-/app/src}
ENV PYTHONPATH ${PYTHONPATH:-/app/src}
EXPOSE ${DOCKER_PORT:-8501}
