FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
ENV PATH="/root/.local/bin:/usr/local/bin:$PATH"

# 1) Update and install base tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    curl \
    wget \
    unzip \
    tmux \
    htop \
    jq \
    gnupg \
    nano \
    && rm -rf /var/lib/apt/lists/*

# 2) Install Python 3.12 from deadsnakes
RUN add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update && apt-get install -y --no-install-recommends \
    python3.12-venv \
    python3.12-dev \
    python3.12-lib2to3 \
    && rm -rf /var/lib/apt/lists/*

# 4) Set Python 3.12 as default for python3 and python
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1 && \
    update-alternatives --set python3 /usr/bin/python3.12 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1 && \
    update-alternatives --set python /usr/bin/python3.12

# 5) Install pip for Python 3.12
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12

# 6) Upgrade pip, setuptools, wheel
RUN python -m pip install --upgrade pip setuptools wheel

# 7) Clean up apt caches
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/*

# 8) Install Poetry
# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3.12 -

# Configure Poetry to not use virtual environments
RUN poetry config virtualenvs.create false
    
# Copy repo to stable folder
COPY . ./stable

# Set a clear root for your project
WORKDIR /stable

# Install deps 
RUN poetry install --with dev --no-interaction --no-ansi

WORKDIR /workspace

CMD ["bash"]