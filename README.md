<br />
<a href="https://bunny.net?ref=pji59zr7a4">
    <img alt="BunnyNet Logo" src="https://bunny.net/v2/images/bunnynet-logo-dark.svg" width="300" />
</a>

# 🖼️ BunnyNet AI

<div align="left">
    <img src="https://img.shields.io/github/v/release/toshy/bunnynet-ai?label=Release&sort=semver" alt="Current bundle version" />
    <a href="https://hub.docker.com/r/t0shy/bunnynet-ai"><img src="https://img.shields.io/badge/Docker%20Hub-t0shy%2Fbunnynet--ai-blue" alt="Docker Hub" /></a>
    <img src="https://img.shields.io/github/actions/workflow/status/toshy/bunnynet-ai/pylint.yml?branch=master&label=Pylint" alt="Code style">
    <img src="https://img.shields.io/badge/Code%20Style-PEP8-orange.svg" alt="Code style" />
    <img src="https://img.shields.io/github/actions/workflow/status/toshy/bunnynet-ai/security.yml?branch=master&label=Security%20check" alt="Security check">
</div>

A basic python app for batch generation of AI created images using [Bunny AI](https://docs.bunny.net/docs/bunny-ai-image-generation).

## Setup

You can choose to either follow the Docker route or plain (Python) route. Images will be saved to the `./output` directory

### 🐋 Docker / Compose

#### Docker

1. Pull the image `t0shy/bunnynet-ai:latest`.

```shell
docker pull t0shy/bunnynet-ai:latest
```

or build from source.

```shell
docker build -t t0shy/bunnynet-ai:latest --no-cache .
```

2. Run it.

```shell
docker run -it -v ${PWD}/output:/app/output --rm t0shy/bunnynet-ai:latest python3 main.py -k "31a98200-02d3-4fdf-888a-c3c1f1758021" -hn "myzone.b-cdn.net" -p "cute pixel art of a bunny with a colorful solid background" -n 5
```

#### Docker Compose

1. Create a `docker-compose.yml`.

```yaml
version: '3.9'

services:
  bunnynet-ai:
    image: t0shy/bunnynet-ai:latest
    volumes:
      - ./output/:/app/output
````

2. Up the service.

```shell
docker compose up -d --remove-orphans
```

3. Run it.


```shell
docker compose run bunnynet-ai python3 main.py -k "489eb71e-1259-4e1a-83c2-2d7859eec469" -hn "myzone.b-cdn.net" -p "cute pixel art of a bunny with a colorful solid background" -n 5
```

### 🐍 Plain

1. Install the requirements with `pip`.

```shell
pip install -r requirements.txt
```

2. Run it.

```shell
python main.py -k "489eb71e-1259-4e1a-83c2-2d7859eec469" -hn "myzone.b-cdn.net" -p "cute pixel art of a bunny with a colorful solid background" -n 5
```

## 🛠️ Contribute

### Prerequisites

* Docker Compose
    * See the Docker Compose [installation guide](https://docs.docker.com/compose/install/) to get started.
* Task
    * See the Task [installation guide](https://taskfile.dev/installation/) to get started

### Pre-commit

Setting up `pre-commit` code style & quality checks for local development.

```shell
pre-commit install
```

### Create service

```shell
task up
```

### Quality & Code Style

```shell
task check
```

### Code Style fix

```shell
task fix
```
