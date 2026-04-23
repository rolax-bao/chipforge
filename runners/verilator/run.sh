#!/usr/bin/env bash
# Verilator runner entrypoint. Expects:
#   /work/design/        — user RTL + testbench files (mounted read-only)
#   /work/out/           — scratch dir for Verilator output (mounted writable)
# Environment:
#   TOP_MODULE  — top-level module name (default: top)
#   TIMEOUT_SEC — hard CPU-time budget (default: 60)
#
# Real orchestration wiring (Celery job spec, resource limits, VCD upload to S3)
# lands in PR #15.

set -euo pipefail

TOP="${TOP_MODULE:-top}"
TIMEOUT="${TIMEOUT_SEC:-60}"
cd /work/out

echo "[verilator-runner] top=${TOP} timeout=${TIMEOUT}s"
echo "[verilator-runner] (placeholder) Real compile/run implemented in PR #15."

timeout "${TIMEOUT}" verilator --version
