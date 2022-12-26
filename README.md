<h1 align="center">BunnyNet AI</h1>

<p align="center" width="100%">
    <img width="32%" src="https://github.com/ToshY/BunnyNet-AI/blob/main/examples/%5Bdemo-cyberpunk-avatar%5Drabbit-18315061651450471761.png" alt="cyberpunk bunny left">
    <img width="32%" src="https://github.com/ToshY/BunnyNet-AI/blob/main/examples/%5Bdemo-cyberpunk-avatar%5Drabbit-395701193653652308.png" alt="cyberpunk bunny middle">
    <img width="32%" src="https://github.com/ToshY/BunnyNet-AI/blob/main/examples/%5Bdemo-cyberpunk-avatar%5Drabbit-13510430255274468932.png" alt="cyberpunk bunny right">
</p>

<div align="center">
    <img src="https://img.shields.io/github/v/release/toshy/bunnynet-ai?label=Release&sort=semver" alt="Current bundle version" />
    <a href="https://hub.docker.com/r/t0shy/bunnynet-ai"><img src="https://img.shields.io/badge/Docker%20Hub-t0shy%2Fbunnynet--ai-blue" alt="Docker Hub" /></a>
    <img src="https://img.shields.io/github/actions/workflow/status/toshy/bunnynet-ai/pylint.yml?branch=main&label=Pylint" alt="Code style">
    <img src="https://img.shields.io/badge/Code%20Style-PEP8-orange.svg" alt="Code style" />
    <img src="https://img.shields.io/github/actions/workflow/status/toshy/bunnynet-ai/security.yml?branch=main&label=Security%20check" alt="Security check" />
    <br /><br />
    <div>Generating images with <a href="https://docs.bunny.net/docs/bunny-ai-image-generation">Bunny AI</a>.</div>
</div>

## Introduction

On December 15th, 2022 BunnyWay
introduced [Bunny AI](https://bunny.net/blog/introducing-bunny-optimizer-ai-a-new-way-of-creating-content/): an easy way
to dynamically generate images using AI technology such as [DALL-E 2](https://openai.com/dall-e-2/) and [Stable Diffusion](https://github.com/CompVis/stable-diffusion)

In order to make it easier to generate images for developers, this (python) application will simply send batch requests based on user's input.

> Note: 
> * This is a **non-official** library for [Bunny AI](https://docs.bunny.net/docs/bunny-ai-image-generation).
> * Bunny AI is currently in [experimental preview phase](https://bunny.net/blog/introducing-bunny-optimizer-ai-a-new-way-of-creating-content/#try-it-out-yourself-).

## Setup

* You can choose to either follow the [Docker](#-docker--compose) or [Python](#-python) route.
* For help, run `main.py -h`.
* Images are always saved in the `./output` directory (relative to the working directory).
  * In the docker container this will be `/app/output`.

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
docker run -it --rm -v ${PWD}/output:/app/output t0shy/bunnynet-ai:latest python3 main.py -k "489eb71e-1259-4e1a-83c2-2d7859eec469" -hn "myzone.b-cdn.net" -p "cute pixel art of a bunny with a colorful solid background" -n 5 -v
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
docker compose run --rm bunnynet-ai python main.py -k "489eb71e-1259-4e1a-83c2-2d7859eec469" -hn "myzone.b-cdn.net" -p "cute pixel art of a bunny with a colorful solid background" -n 5 -v
```

4. Saved images can be found on the mounted directory of the host machine.
   * Filename format is as follows: `[{image_blueprint}]{slug_prompt}-{seed}.{file_extension}`.

### 🐍 Python

1. Install the requirements with `pip`.

```shell
pip install -r requirements.txt
```

2. Run it.

```shell
python main.py -k "489eb71e-1259-4e1a-83c2-2d7859eec469" -hn "myzone.b-cdn.net" -p "cute pixel art of a bunny with a colorful solid background" -n 5 -v
```

3. Saved images can be found in the `./output` directory (relative to working directory).
   * Filename format is as follows: `[{image_blueprint}]{slug_prompt}-{seed}.{file_extension}`.

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

### Checks

```shell
task contribute
```

> Note: you can use `task tools:black:fix` to resolve codestyle issues.

## ❕ License

This repository comes with the [MIT license](https://choosealicense.com/licenses/mit/).
