FROM ghcr.io/qtvhao/torchaudio-triton-cpu-only:latest
ENV STABLE_TS_MODEL=tiny
# // tiny	39 M	tiny.en	tiny	~1 GB	~32x
# // base	74 M	base.en	base	~1 GB	~16x
# // small	244 M	small.en	small	~2 GB	~6x
# // medium	769 M	medium.en	medium	~5 GB	~2x
# // large	1550 M	N/A	large	~10 GB	1x

ENV STABLE_TS_LANGUAGE=vi

COPY pyproject.toml poetry.lock ./
ENV PATH="/root/.local/bin:${PATH}"
RUN poetry config virtualenvs.create false
RUN poetry install
ENV PATH="/root/.local/share/pypoetry/venv/bin:${PATH}"
# 
RUN pip3 install -U stable-ts --no-cache-dir

COPY ./tests/ ./tests/
RUN stable-ts --model tiny --device cpu -y tests/synthesize-result-2532432836.mp3
COPY *.py ./
RUN pytest ./test_audio_operations.py -vv

CMD [ "gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "app:create_app"]
