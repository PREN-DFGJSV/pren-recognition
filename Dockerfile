FROM hdgigante/python-opencv:4.9.0-ubuntu

ENV SERVER_PORT=8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt
COPY src/ src/
COPY res/ res/

RUN pip install -r requirements.txt --break-system-packages

EXPOSE $SERVER_PORT

CMD python3 -m src.main
