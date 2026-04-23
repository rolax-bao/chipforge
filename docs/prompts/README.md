# Prompt templates

Each prompt template is a YAML file loaded by `apps/api/chipforge_api/ai/`. Real templates land in PR #7 (chat/complete) and PR #13 (testbench, spec→rtl).

Naming convention: `<intent>.<domain>.yaml`, e.g. `chat.verilog.yaml`, `generate.testbench.yaml`.
