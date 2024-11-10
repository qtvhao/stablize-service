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

RUN curl -sSL https://install.python-poetry.org | python3 -
COPY pyproject.toml poetry.lock ./
ENV PATH="/root/.local/bin:${PATH}"
RUN poetry config virtualenvs.create false
RUN poetry install
ENV PATH="/root/.pyenv/versions/${PYTHON_VERSION}/bin:${PATH}"
ENV PATH="/root/.local/share/pypoetry/venv/bin:${PATH}"
RUN pip3 install torch==2.5.1 torchaudio==2.5.1 --index-url  https://download.pytorch.org/whl/cpu --no-cache-dir
RUN pip3 install triton==2.3.1 --no-cache-dir
RUN pip3 install -U stable-ts --no-cache-dir
RUN apt update && apt install -y ffmpeg --no-install-recommends && apt clean && rm -rf /var/lib/apt/lists/*
# RUN pip3 install -U numpy --no-cache-dir

ENV PATH="/root/.local/bin:${PATH}"

# RUN find / -name stable-ts ; exit 1
COPY ./tests/ ./tests/
RUN stable-ts --model tiny --device cpu -y tests/synthesize-result-2532432836.mp3
COPY *.py ./
RUN pytest ./test_audio_operations.py -vv

CMD [ "gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "app:create_app"]
