FROM python
RUN apt update
RUN apt install python3 -y && apt install python3-pip -y
RUN ln -sf /usr/bin/python3 /usr/bin/python
RUN ln -sf /usr/bin/pip3 /usr/bin/pip

EXPOSE 8000
WORKDIR /app/sphinx
COPY requirements.txt /app/sphinx/
RUN PIP_EXTRA_INDEX_URL=http://10.42.0.35:8080/simple/ pip install -r /app/sphinx/requirements.txt --trusted-host 10.42.0.35
COPY ./instantclient /opt/instantclient/
RUN cd /opt/instantclient
RUN ls -al /opt/instantclient
RUN apt install libaio1

ENV LD_LIBRARY_PATH=/opt/instantclient
COPY . /app/sphinx/
RUN mkdir -p /opt/envs/sphinx.lionx.com.br
ENTRYPOINT ["python","/app/sphinx/main.py"]
