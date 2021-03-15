FROM ubuntu:16.04

RUN apt-get -y update && apt-get install -y --no-install-recommends \
	python3 \
	python3-pip \
	git

# RUN pip3 install --upgrade pip 
# RUN pip3 install setuptools

# To build image:
# docker build . -t pg-gan
# To run: 
# docker run -it -v <full_path_to_pg-gan>:<full_path_to_pg-gan> pg-gan bash