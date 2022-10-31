FROM python:latest
COPY ./ /home
RUN pip install -r /home/requirements.txt
WORKDIR /home
CMD [ "python", "./bot.py"]