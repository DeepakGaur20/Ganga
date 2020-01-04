**OPC UA Server – Sine wave generation DGS**

**Language:** Python – 3.7.4

Deployment Env. Docker

**Modules:**

- python-opcua ([https://python-opcua.readthedocs.io/en/latest/](https://python-opcua.readthedocs.io/en/latest/))
- numpy – to generate sin wave

**Security:**

- Self-signed x509 certificate
- Basic authentication (username,password)

**Project structure:**

- Server.py :- OPC UA server(sine wave generation)
- Client.py :- Client code to test all server functionalities
- Certificate.pem :- Self-signed x509 certificate
- Key.pem :- Private key for the certificate
- Dockerfile :- Dockerfile to build docker image
- Makefile :- Script to auto build and deploy server

**Getting started**

**Run below commands in a terminal to start OPC UA server in docker container:**

- $make image
- $make run
- $make log
- Run Below

**Run below command to start client:**

$pip install opcua numpy cryptography

$python client.py

**#NOTE: you can change the value of frequency to be setup on the server in the client.py file**
