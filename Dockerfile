# python:3.12.16-slim-bookworm, pinned by its multi-arch index digest
FROM python:3.12.16-slim-bookworm@sha256:e697c81897302a4c4333bade000d98038fbb21eb064f8ee1fd42d02ebcd9d337

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=120

WORKDIR /processor

# PyTorch build: cpu or cuda. app.yml's variants set it (cpu variant: CPU-only torch 2.14.1 from the
# PyTorch CPU index, no NVIDIA libraries; gpu variant: torch 2.14.1+cu126, which runs on the platform's
# GPU nodes: Amazon Linux 2 ECS GPU AMI, NVIDIA driver 550 = CUDA 12.4). The default is cpu for a
# builder that passes no build arguments. On the cuda build the app exits 1 when it sees no GPU.
ARG TORCH_FLAVOUR=cpu

# The complete pinned dependency set (no resolver: see requirements.txt); binary wheels only, except
# docrep (a pure-Python sdist, no wheel published).
COPY requirements.txt requirements-${TORCH_FLAVOUR}.txt /processor/
RUN pip install --no-deps --only-binary=:all: --no-binary=docrep \
        -r /processor/requirements.txt -r /processor/requirements-${TORCH_FLAVOUR}.txt \
    && find /usr/local/lib/python3.12/site-packages -name '*.pyc' -delete \
    && find /usr/local/lib/python3.12/site-packages -path '*/torch/*' -prune -o -type d -name tests -prune -exec rm -rf {} + \
    && rm -rf /usr/local/lib/python3.12/site-packages/torch/include

COPY processor/ /processor/processor/
COPY VERSION /processor/VERSION

ENV PYTHONPATH="/processor" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HOME=/tmp \
    MPLBACKEND=Agg \
    MPLCONFIGDIR=/tmp/matplotlib \
    NUMBA_CACHE_DIR=/tmp/numba \
    XDG_CACHE_HOME=/tmp/cache \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility \
    TORCH_FLAVOUR=${TORCH_FLAVOUR}

# Build matplotlib's font cache and import the stack once, so a run needs no writes outside /tmp and
# no network (no CellTypist pretrained models are bundled or downloaded; see README "Licences").
RUN python -c "import matplotlib.pyplot, scanpy, scvi, celltypist, skmisc" \
    && mkdir -p /tmp/matplotlib /tmp/numba /tmp/cache && chmod -R a+rwX /tmp/matplotlib /tmp/numba /tmp/cache

# Runs as uid 1000 on the platform; nothing here needs root. PyTorch looks the user up (getpass), so
# uid 1000 gets a passwd entry.
RUN useradd --uid 1000 --no-create-home --home-dir /tmp --shell /usr/sbin/nologin processor
USER 1000

ENTRYPOINT ["python3", "-m", "processor.entry"]
