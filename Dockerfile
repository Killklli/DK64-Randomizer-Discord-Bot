FROM python:latest
WORKDIR /home
COPY ./ /home
RUN pip install -r /home/requirements.txt
RUN git clone https://github.com/2dos/DK64-Randomizer-Dev.git
RUN git clone https://github.com/2dos/DK64-Randomizer-Release.git
CMD [ "python", "./bot.py"]