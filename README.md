<a name="top"></a>

[![CI/CD (GitHub Container Registry)](https://github.com/PREN-DFGJSV/PREN_Recognition/actions/workflows/docker.yml/badge.svg)](https://github.com/PREN-DFGJSV/PREN_Recognition/actions/workflows/docker.yml)

<br/>
<div align="center">
  <a href="https://github.com/PREN-DFGJSV/PREN_Recognition">
    <img src="docs/images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">PREN Cube Recognition</h3>

  <p align="center">
    Hochschule Luzern, Modul PREN (Produktentwicklung)
    <br/>
    <a href="https://drive.google.com/drive/u/0/folders/1zobs-a9jfQnSiirycorRd-K4Mo74t9py">PREN1 Dokumente</a>
    ·
    <a href="https://github.com/orgs/PREN-DFGJSV/packages">GitHub Container Registry</a>
  </p>
</div>

## Docker

Starte den Docker Container, welcher das Docker Image von der GitHub Container Registry bezieht:
```sh
docker compose up
```

Beende den Docker Container:
```sh
docker compose down
```

Aktualisierung erzwingen:
```sh
docker-compose pull
docker-compose up --force-recreate --build --no-deps
```

Im Browser öffnen:
```sh
http://127.0.0.1:5000/start
```

### Or manual build and run
```sh
docker build -t pren/recognition:latest .
docker run -p 5000:5000 -e DEPLOY_ENV='prod' -e PYTHONUNBUFFERED='1' -e PORT='5000' pren/recognition:latest
```

pren-420709

```sh
docker build -t pren/recognition:latest .
docker run -p 5000:5000 -e DEPLOY_ENV='prod' -e PYTHONUNBUFFERED='1' -e PORT='5000' -e VALIDATION_URL='https://ubqs3u6r81.execute-api.eu-central-1.amazonaws.com' pren/recognition:latest
docker run -p 5000:5000 -e DEPLOY_ENV='prod' -e PYTHONUNBUFFERED='1' -e PORT='5000' -e VALIDATION_URL='https://ubqs3u6r81.execute-api.eu-central-1.amazonaws.com' -e MESSPUNKT_OBEN_RECHTS_X='255' -e MESSPUNKT_UNTEN_LINKS_Y='195' -e MESSPUNKT_UNTEN_RECHTS_X='255' -e MESSPUNKT_UNTEN_RECHTS_Y='175' -e USE_STATIC_ROTATIONSPUNKT="False" pren/recognition:latest
```

### Urls
- http://localhost:5000/reset
- http://localhost:5000/start
- results:
- - http://localhost:5000/1/result
- - http://localhost:5000/2/result
- - http://localhost:5000/3/result

## Docker cloud
- Cloud Run: https://console.cloud.google.com/run?hl=en&project=pren-420709
- - Config: pren-recognition > Edit & deploy new revision > Container image URL > gcr.io/pren-420707/pren-recognition > "Select most recent" > Deploy
- URL (Reset): https://pren-recognition-r35oqtcxna-oa.a.run.app/reset
- - Start: https://pren-recognition-r35oqtcxna-oa.a.run.app/start
- - Result 1: https://pren-recognition-r35oqtcxna-oa.a.run.app/1/result
- Logs: https://cloudlogging.app.goo.gl/9e8VreZX2VDB5dUx8 | https://console.cloud.google.com/run/detail/europe-west6/pren-recognition/logs?hl=en&project=pren-420709


## Setup

Run locally
```sh
python -m src.main
```

Save dependencies
```sh
pip freeze > requirements.txt
```

Build docker locally
```sh
docker build . -t recognition:latest
docker run -d recognition:latest
```