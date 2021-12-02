FROM python:3.8

WORKDIR /workspace

COPY requirements.txt /workspace/requirements.txt
RUN pip install -U pip && pip install --upgrade setuptools
RUN pip install -r /workspace/requirements.txt -U
