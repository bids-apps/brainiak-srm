FROM ubuntu:16.04

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
                        git \
                        libfreetype6-dev \
                        mpich \
                        pkg-config \
                        python3-pip \
                        python3-tk \
    && pip3 install --no-cache-dir -U \
                    pip \
    && pip3 install --no-cache-dir \
                    git+https://github.com/IntelPNI/brainiak \
                    nibabel \
                    nilearn

RUN mkdir -p /code \
    mkdir /oasis \
    mkdir /projects \
    mkdir /scratch \
    mkdir /local-scratch
COPY run.py /code/run.py

ENTRYPOINT ["/code/run.py"]
