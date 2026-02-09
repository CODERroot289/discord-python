FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock* ./

RUN pip install uv     && if [ -f uv.lock ]; then uv sync --locked --no-dev --no-install-project; else uv sync --no-dev --no-install-project; fi

COPY . .

CMD ["python", "main.py"]