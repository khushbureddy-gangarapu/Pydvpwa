FROM gcr.io/oss-fuzz-base/base-builder-python:v1
RUN apt-get update && apt-get install -y make autoconf automake libtool
RUN git clone \
	--depth 1 \
	--branch main \
	https://github.com/ultrajson/ultrajson.git
 
RUN apt-get install qtbase5-dev
RUN pip3 install pyqt5
RUN pip3 install --upgrade pip
RUN pip3 install hypothesis
RUN pip3 install lz4 --force
RUN pip3 install idna --force
RUN pip3 install atheris --force


COPY . $SRC/Pydvpwa
WORKDIR Pydvpwa
COPY .clusterfuzzlite/build.sh .clusterfuzzlite/json_differential_fuzzer.py .clusterfuzzlite/target_fuzzer.py .clusterfuzzlite/hypothesis_structured_fuzzer.py $SRC/
