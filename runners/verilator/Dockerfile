# syntax=docker/dockerfile:1.7
# Server-side Verilator runner.
# Invoked by the job orchestrator (PR #15) for workloads too heavy for WASM.

FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        verilator \
        g++ \
        make \
        python3 \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /work

COPY run.sh /usr/local/bin/run.sh
RUN chmod +x /usr/local/bin/run.sh

# Safety: runner containers are invoked with read-only root FS and a scratch
# /work volume. `run.sh` is the only entrypoint.
ENTRYPOINT ["/usr/local/bin/run.sh"]
