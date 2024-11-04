FROM python:3.11

RUN apt-get update && \
    apt-get install -y locales vim less libopus0 ffmpeg libc6 && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8 && \
    apt-get clean

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN pip install --upgrade pip setuptools
RUN python -m pip install discord.py jupyterlab arxiv pandas matplotlib numpy
