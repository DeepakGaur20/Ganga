
all: image run log

image:
	 docker build -t sineopcua:latest .

run:
	docker run -p 4840:4840 -d --name opcua sineopcua:latest

log:
	docker logs -f opcua

