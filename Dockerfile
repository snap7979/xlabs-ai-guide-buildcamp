FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:0.12.22 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml uv.lock .python-version README.md ./
COPY app.py agent.py tools.py ./
COPY data/kubernetes_scenarios.json data/kubernetes_troubleshooting_docs.json ./data/

RUN uv sync --frozen --no-dev

EXPOSE 8501

CMD ["uv", "run", "--no-sync", "streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
