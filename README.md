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

1. Beziehe das Docker Image von der GitHub Container registry:
   ```sh
   docker compose up
   ```
2. Erstelle einen Docker Container aus dem Image und führe diesen aus:
   ```sh
   docker compose down
   ```

Aktualisierung erzwingen:
```sh
docker-compose pull
docker-compose up --force-recreate
```

## Setup

Dependencies
```sh
pip freeze > requirements.txt
```

Build locally
```sh
docker build . -t recognition:latest
docker run -d recognition:latest
```