FROM ubuntu:18.04
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt update
RUN apt install -y --no-install-recommends python3-dev python3-setuptools build-essential

RUN apt install -y --no-install-recommends wget iputils-ping iproute2 dnsutils
RUN apt install -y --no-install-recommends less vim

RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y python3.7
RUN ln -sf /usr/bin/python3.7 /usr/bin/python3
RUN wget https://bootstrap.pypa.io/get-pip.py --no-check-certificate && python3 get-pip.py
RUN pip3 install --upgrade pip

COPY src/server-requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN rm -f requirements.txt


RUN groupadd xs-agent --gid 1000 --non-unique && \
    useradd xs-agent -m --home-dir /opt/xs-agent --uid 2000 --gid 1000 --non-unique

# RUN apt install -y sudo
# RUN echo "ad-service ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ad-service

USER xs-agent:xs-agent

COPY --chown=xs-agent:xs-agent src/ /opt/xs-agent/app
ENV PYTHONPATH /opt/xs-agent/app


WORKDIR /opt/xs-agent/app
EXPOSE 8000

# use the entrypoint to work around the dns problem for now
CMD ./server.sh start
# ENTRYPOINT ["/boot.sh"]
# CMD ["run"]

