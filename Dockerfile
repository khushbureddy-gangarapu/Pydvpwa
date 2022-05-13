FROM gcr.io/oss-fuzz-base/base-builder-python:v1
RUN apt-get update && apt-get install -y make autoconf automake libtool
RUN git clone https://github.com/ultrajson/ultrajson.git
RUN pip3 install --upgrade pip
RUN pip3 install hypothesis
RUN pip3 install lz4 --force
RUN pip3 install idna --force
RUN pip3 install atheris --force


COPY . $SRC/Pydvpwa
WORKDIR Pydvpwa
COPY .clusterfuzzlite/build.sh json_differential_fuzzer.py target_fuzzer.py hypothesis_structured_fuzzer.py $SRC/
