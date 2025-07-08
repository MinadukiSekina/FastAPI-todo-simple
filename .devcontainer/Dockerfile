FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_CACHE_DIR=/workspace/.cache/uv \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/home/vscode/.venv \
    UV_COMPILE_BYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    git \
    jq \
    ca-certificates \
    build-essential \
    ripgrep \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (for additional development tools)
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt-get install -y nodejs
