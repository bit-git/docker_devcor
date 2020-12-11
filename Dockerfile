FROM python:alpine3.12

RUN apk update && apk upgrade && apk add openssl-dev openssh

WORKDIR /root/dev-workspace/
COPY . .

RUN python -m pip install -r requirements.txt
RUN rm requirements.txt
RUN mkdir /root/.ssh && mv /root/dev-workspace/ssh_config /root/.ssh/config

EXPOSE 8080 

CMD ["cat", "lab_env"]


# sudo docker run -t -d -p 8000:8080 --name samplerunning devcor
# docker run -it -p 8080:8080 --rm devcor