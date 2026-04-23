# @chipforge/verilog-lang

Monaco language contribution for Verilog-2005 / SystemVerilog.

Current skeleton exports the keyword list only. In PR #6 this package will add:

- Monarch tokenizer for syntax highlighting
- Tree-sitter WASM bindings for semantic features (symbol index, go-to-definition, rename)
- Basic snippets (module, always_ff, FSM template)
