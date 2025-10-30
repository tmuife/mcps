FROM python:3.12-slim

WORKDIR /mcp

COPY dbtools-mcp-server.py /mcp/
COPY pyproject.toml /mcp/
COPY uv.lock /mcp/
#COPY .env.prod /app/.env 

#RUN apt-get update && apt-get install -y && apt-get install ffmpeg -y \
#    build-essential libsndfile1 \
#    && rm -rf /var/lib/apt/lists/*

RUN pip install uv 
RUN uv sync -v && uv pip list

HEALTHCHECK --interval=30s --timeout=10s CMD curl -f http://localhost:8000/mcp || exit 1

CMD [".venv/bin/python", "dbtools-mcp-server.py", "--transport", "http", "--host", "0.0.0.0", "--port", "8000"]   