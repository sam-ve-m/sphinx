FROM python
RUN apt update
RUN apt install python3 -y && apt install python3-pip -y
RUN ln -sf /usr/bin/python3 /usr/bin/python
RUN ln -sf /usr/bin/pip3 /usr/bin/pip
ENV PIP_EXTRA_INDEX_URL=http://10.42.0.129:8080/simple/

COPY requirements.txt /app/sphinx/
RUN pip install -r /app/sphinx/requirements.txt --trusted-host 10.42.0.129
COPY . /app/sphinx/

WORKDIR /app/sphinx

ENTRYPOINT ["python","/app/sphinx/main.py"]
