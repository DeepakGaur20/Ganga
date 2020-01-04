FROM python:3.7.4

COPY . .
RUN pip install --upgrade pip
RUN pip install numpy opcua cryptography

CMD [ "python", "server.py" ]
