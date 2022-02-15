FROM python:3.8 AS builder
COPY requirements.txt .

RUN pip install wheel
RUN pip install --user -r requirements.txt

FROM python:3.8-slim
COPY --from=builder /root/.local /root/.local
WORKDIR /app

RUN apt-get update
RUN apt-get install libpq5 -y
RUN apt-get install libaio1 -y

COPY ./instantclient /opt/instantclient/
RUN cd /opt/instantclient
RUN ls -al /opt/instantclient

RUN mkdir -p /opt/envs/sphinx.lionx.com.br/
RUN mkdir -p /opt/envs/heimdall.lionx.com.br/
RUN mkdir -p /opt/envs/mist.lionx.com.br/
RUN touch /opt/envs/sphinx.lionx.com.br/.env
RUN touch /opt/envs/heimdall.lionx.com.br/.env
RUN touch /opt/envs/mist.lionx.com.br/.env
RUN mkdir -p /app/logs/

COPY . .
ENV PATH=/root/.local:$PATH
RUN pip install --upgrade pip
RUN python -m pip install --upgrade pip
ENV LD_LIBRARY_PATH=/opt/instantclient
ENTRYPOINT ["python", "/app/main.py"]