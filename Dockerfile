FROM python:3.8 AS builder
COPY requirements.txt .

ARG oci_nexus_password

RUN mkdir -p ~/.pip/
RUN touch ~/.pip/pip.conf

RUN echo "[global]" >> ~/.pip/pip.conf
RUN echo "timeout = 60" >> ~/.pip/pip.conf
RUN echo "extra-index-url =" >> ~/.pip/pip.conf
RUN echo "    https://backend:${oci_nexus_password}@nexus.sigame.com.br/repository/pypi/simple" >> ~/.pip/pip.conf

RUN pip install wheel
RUN pip install --upgrade pip
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
RUN mkdir -p /opt/envs/etria.lionx.com.br/
RUN mkdir -p /opt/envs/persephone.client.python.lionx.com.br/
RUN mkdir -p /opt/envs/mepho.lionx.com.br/
RUN touch /opt/envs/sphinx.lionx.com.br/.env
RUN touch /opt/envs/heimdall.lionx.com.br/.env
RUN touch /opt/envs/mist.lionx.com.br/.env
RUN touch /opt/envs/etria.lionx.com.br/.env
RUN touch /opt/envs/persephone.client.python.lionx.com.br/.env
RUN touch /opt/envs/mepho.lionx.com.br/.env
RUN mkdir -p /app/logs/

COPY . .
ENV PATH=/root/.local:$PATH
RUN pip install --upgrade pip
RUN python -m pip install --upgrade pip
ENV LD_LIBRARY_PATH=/opt/instantclient
ENTRYPOINT ["python", "/app/main.py"]