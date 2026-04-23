# @chipforge/eda-wasm

Browser-side wrappers around WASM EDA tools:

| Tool              | Source                                                                                | Lands in |
| ----------------- | ------------------------------------------------------------------------------------- | -------- |
| iverilog          | custom WASM build                                                                     | PR #10   |
| yosys             | [YoWASP/yosys](https://github.com/YoWASP/yosys)                                       | PR #16   |
| verible-lint      | [chipsalliance/verible](https://github.com/chipsalliance/verible) (experimental WASM) | PR #14   |
| Surfer (waveform) | [surfer-project/surfer](https://gitlab.com/surfer-project/surfer)                     | PR #11   |

All runners share the `EdaRunner` interface so `apps/web` can dispatch to whichever backend (Web Worker WASM or server sandbox) is best for the workload.
