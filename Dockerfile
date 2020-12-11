FROM python:alpine3.12

RUN apk update && apk upgrade && apk add openssl-dev openssh

WORKDIR /root/docker_devcor/


RUN python -m pip install -r requirements.txt
RUN rm requirements.txt
RUN git clone https://github.com/bit-git/docker_devcor.git
RUN mkdir /root/.ssh && mv /root/docker_devcor/ssh_config /root/.ssh/config

EXPOSE 8080 

CMD ["sh"]


# sudo docker run -t -d -p 8000:8080 --name samplerunning devcor
# docker run -it -p 8080:8080 --rm devcor