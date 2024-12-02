FROM python:3.10-slim

WORKDIR /usr/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

RUN pip freeze

ENTRYPOINT ["./entrypoint.sh"]
