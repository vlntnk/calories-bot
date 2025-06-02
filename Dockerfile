FROM python:3.13.3

ENV PYTHONDONTWRITEBYTECODE=1\
    PYTHONBUFFERED=1

USER root

RUN apt-get update && apt-get install --no-install-recommends -y\
    curl \
    netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV APP_DIR=/home/$USER/bot
WORKDIR $APP_DIR

#RUN chown -R "$USER":"$USER" $APP_DIR

COPY . $APP_DIR 
RUN pip install -r requirements.txt

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

CMD ["python3", "main.py"]
