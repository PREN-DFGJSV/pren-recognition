FROM hdgigante/python-opencv:4.9.0-ubuntu

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt
COPY src/ src/
COPY res/ res/

RUN apt-get update && apt-get install -y sudo
RUN sudo apt-get install python3-tk -y
RUN sudo pip install -r requirements.txt --break-system-packages

CMD python3 -m src.main
