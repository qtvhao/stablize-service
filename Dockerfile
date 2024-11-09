FROM ghcr.io/qtvhao/debian-smb:main
RUN echo "deb http://mirror.sg.gs/debian/ bookworm main contrib non-free" > /etc/apt/sources.list
RUN echo "deb http://mirror.sg.gs/debian/ bookworm-updates main contrib non-free" >> /etc/apt/sources.list
WORKDIR /app/

ENV STABLE_TS_MODEL=tiny
# // tiny	39 M	tiny.en	tiny	~1 GB	~32x
# // base	74 M	base.en	base	~1 GB	~16x
# // small	244 M	small.en	small	~2 GB	~6x
# // medium	769 M	medium.en	medium	~5 GB	~2x
# // large	1550 M	N/A	large	~10 GB	1x

ENV STABLE_TS_LANGUAGE=vi
USER root

# Set environment variables
ENV PYTHON_VERSION=3.10.15

# Update package list and install dependencies
RUN apt-get update && \
    apt-get install -y \
    ffmpeg \
    curl \
    git \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    python3-openssl \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN curl https://pyenv.run | bash

RUN apt-get update && apt-get install -y build-essential
ENV PATH="/root/.pyenv/bin:${PATH}"
RUN pyenv install ${PYTHON_VERSION} \
    && pyenv global ${PYTHON_VERSION} \
    && pyenv rehash

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 \
    && update-alternatives --install /usr/bin/pip3 pip3 /usr/bin/pip3 1

RUN curl -sSL https://install.python-poetry.org | python3 -
COPY pyproject.toml poetry.lock ./
RUN /root/.local/bin/poetry install

COPY ./tests/all.txt ./tests/in.wav ./
RUN stable-ts in.wav --model ${STABLE_TS_MODEL} --language ${STABLE_TS_LANGUAGE} --align all.txt --overwrite --output ni.json
# RUN stable-ts in.wav --model ${STABLE_TS_MODEL} --language ${STABLE_TS_LANGUAGE} --align all.txt --overwrite --output ni.json -fw

CMD [ "gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "app:create_app"]
