FROM ghcr.io/qtvhao/torch:main

RUN apt-get update && apt-get install -y ffmpeg
WORKDIR /app/

ENV STABLE_TS_MODEL=tiny
# // tiny	39 M	tiny.en	tiny	~1 GB	~32x
# // base	74 M	base.en	base	~1 GB	~16x
# // small	244 M	small.en	small	~2 GB	~6x
# // medium	769 M	medium.en	medium	~5 GB	~2x
# // large	1550 M	N/A	large	~10 GB	1x

ENV STABLE_TS_LANGUAGE=vi
COPY ./tests/all.txt ./tests/in.wav ./
# 
RUN stable-ts in.wav --model ${STABLE_TS_MODEL} --language ${STABLE_TS_LANGUAGE} --align all.txt --overwrite --output ni.json
# RUN stable-ts in.wav --model ${STABLE_TS_MODEL} --language ${STABLE_TS_LANGUAGE} --align all.txt --overwrite --output ni.json -fw
