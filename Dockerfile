FROM python:3.10-slim

WORKDIR /usr/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint_api.sh
RUN chmod +x entrypoint_worker.sh

RUN pip freeze
