FROM python:3.8

ENV LANG C.UTF-8

RUN mkdir /code
COPY . /code

RUN cp /usr/share/zoneinfo/Asia/Shanghai  /etc/localtime
#RUN cp /usr/share/zoneinfo/Asia/Shanghai  /etc/localtime \
#&& cp /code/sources.list /etc/apt/ \
#&& apt-get update \
#&& apt-get -y --allow upgrade

WORKDIR /code

RUN pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/ \
&& pip install -r requirement.txt -i https://mirrors.aliyun.com/pypi/simple/

ENTRYPOINT ["python", "run.py"]