FROM python:3.9.6-slim-buster

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update  \
	&& apt upgrade -yqq

ENV TWITTER_BEARER_TOKEN=${TWITTER_BEARER_TOKEN}
WORKDIR /app
COPY stock-ticker-bot.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["stock-ticker-bot.py"]
