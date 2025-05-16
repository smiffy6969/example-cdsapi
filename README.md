# FastAPI MVC

## Usage

### Setup vitrual env locally

Create virtual environment

```bash
python -m venv .venv
```

Activate virtual environment

```bash
source .venv/bin/activate
```

Once finished working, deactivate virtual environment

```bash
deactivate
```

Install dependencies

```bash
pip install -r requirements.txt
```
### Develop on Dev server

```bash
fastapi dev main.py
```

### Run server

```bash
fastapi run main.py
```

## Run in Docker

```bash
docker build -t fastapi-mvc .
docker run -d -p 8000:8000 fastapi-mvc
```

## Using Docker Compose

```bash
docker-compose up --build
```



