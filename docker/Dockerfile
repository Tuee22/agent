# -----------------------------------------------------------------------------
# Development container for the *agent* project
# -----------------------------------------------------------------------------
FROM python:3.12-slim

# Install Poetry globally (easy path, avoids custom PATH handling issues)
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN pip install --upgrade pip && \
    pip install "poetry==1.8.2"

WORKDIR /workspace

# Copy project metadata first (leverages Docker-layer caching)
COPY pyproject.toml README.md ./
RUN poetry install --only main --no-root

# Bring in source code and dev tools
COPY src ./src
RUN poetry install --only dev

CMD ["bash"]
