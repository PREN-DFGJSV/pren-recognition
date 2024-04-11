# FROM hdgigante/python-opencv:4.9.0-ubuntu # Unable to establish RTSP connection
FROM python:3.12.3

WORKDIR /app

RUN apt-get update && apt-get install -y libgl1-mesa-glx && apt-get install python3-tk -y

COPY requirements.txt .
COPY src/ src/

RUN pip install --no-cache-dir -r requirements.txt

CMD python3 -m src.main