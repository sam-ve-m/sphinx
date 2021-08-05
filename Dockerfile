FROM python
RUN apt update
RUN apt install python3 -y && apt install python3-pip -y
RUN ln -sf /usr/bin/python3 /usr/bin/python
RUN ln -sf /usr/bin/pip3 /usr/bin/pip

EXPOSE 8000
RUN mkdir -p /opt/envs/sphinx.lionx.com.br/
RUN mkdir -p /opt/envs/heimdall.lionx.com.br/
RUN touch /opt/envs/sphinx.lionx.com.br/.env
RUN touch /opt/envs/heimdall.lionx.com.br/.env
WORKDIR /app/sphinx
COPY ./requirements.txt /app/sphinx/
COPY ./instantclient /opt/instantclient/
RUN cd /opt/instantclient
RUN ls -al /opt/instantclient
RUN apt install libaio1

ENV LD_LIBRARY_PATH=/opt/instantclient
COPY . /app/sphinx/
RUN mkdir -p /opt/envs/sphinx.lionx.com.br
ENTRYPOINT ["python","/app/sphinx/main.py"]

