# Regex Generator API

A FastAPI-based microservice that uses an LLM (via [g4f](https://pypi.org/project/g4f/)) to generate and validate regular expressions based on user-provided text descriptions. The system includes optional proxy support and can be run in a Dockerized environment.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Endpoints](#endpoints)
- [Development](#development)

## Introduction

This service takes a natural language description of a pattern and returns a generated regex with an accompanying validation script. It uses LLMs via `g4f`, and supports proxy rotation for request anonymization or access management.

## Features

- Natural language to regex generation using GPT-4o-mini.
- Validation of generated regex using embedded test code.
- Proxy rotation support (configured via `assets/proxy.txt`).
- REST API with FastAPI.
- Dockerized for easy deployment.

## Installation

### Requirements

- Docker and Docker Compose
- Python 3.11 (for local runs)

### Using Docker

```bash
docker-compose up --build
```

### Local Development

```bash
pip install -r requirements.txt
python app/main.py
```

## Usage

Access the service at [http://localhost:8000](http://localhost:8000). A basic frontend is available at `/`, served from `static/index.html`.

Send a POST request to `/generate` with JSON:

```json
{
  "problem": "Find all emails in a string"
}
```

## Configuration

- **Proxies:** Configure in `assets/proxy.txt` (optional).
- **System Prompt:** Define LLM behavior in `assets/prompt.txt`.

## Endpoints

- `GET /` – Serve the static frontend.
- `POST /generate` – Generate and validate a regex based on input prompt.

## Development

Key modules:

- `ai_worker.py` – Handles LLM calls with retry and history.
- `regex_service.py` – Handles regex generation and validation.
- `regex_controller.py` – API controller.
- `proxy_provider.py` – Manages proxy list.