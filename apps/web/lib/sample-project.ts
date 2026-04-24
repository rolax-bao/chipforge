export type LanguageId = 'verilog' | 'systemverilog' | 'markdown' | 'plaintext';

export type FileEntry = {
  path: string;
  content: string;
  language: LanguageId;
};

export const SAMPLE_PROJECT_NAME = 'example-project';

export const SAMPLE_FILES: FileEntry[] = [
  {
    path: 'rtl/counter.v',
    language: 'verilog',
    content: `// counter.v — 4-bit up counter with synchronous reset
module counter (
    input  wire       clk,
    input  wire       rst_n,
    output reg  [3:0] q
);
    always @(posedge clk) begin
        if (!rst_n) q <= 4'd0;
        else        q <= q + 4'd1;
    end
endmodule
`,
  },
  {
    path: 'tb/counter_tb.v',
    language: 'verilog',
    content: `// counter_tb.v — minimal testbench for counter.v
\`timescale 1ns/1ps

module counter_tb;
    reg         clk = 0;
    reg         rst_n = 0;
    wire [3:0]  q;

    counter dut (.clk(clk), .rst_n(rst_n), .q(q));

    always #5 clk = ~clk;

    initial begin
        $dumpfile("counter_tb.vcd");
        $dumpvars(0, counter_tb);
        #12 rst_n = 1;
        #200 $finish;
    end
endmodule
`,
  },
  {
    path: 'rtl/alu.sv',
    language: 'systemverilog',
    content: `// alu.sv — tiny SystemVerilog ALU for smoke-testing the editor
typedef enum logic [1:0] {
    ALU_ADD = 2'b00,
    ALU_SUB = 2'b01,
    ALU_AND = 2'b10,
    ALU_OR  = 2'b11
} alu_op_e;

module alu #(parameter int WIDTH = 8) (
    input  logic [WIDTH-1:0] a,
    input  logic [WIDTH-1:0] b,
    input  alu_op_e          op,
    output logic [WIDTH-1:0] y,
    output logic             zero
);
    always_comb begin
        unique case (op)
            ALU_ADD: y = a + b;
            ALU_SUB: y = a - b;
            ALU_AND: y = a & b;
            ALU_OR : y = a | b;
        endcase
    end
    assign zero = (y == '0);
endmodule
`,
  },
  {
    path: 'README.md',
    language: 'markdown',
    content: `# example-project

A tiny scratch project to exercise the ChipForge editor.

- \`rtl/counter.v\` — a 4-bit up counter (Verilog-2001)
- \`tb/counter_tb.v\` — a minimal testbench
- \`rtl/alu.sv\` — a SystemVerilog ALU, to smoke-test SV highlighting

File CRUD and persistence land in PR #5. Edits here live only in memory.
`,
  },
];

export function filesByPath(files: FileEntry[]): Record<string, FileEntry> {
  return Object.fromEntries(files.map((f) => [f.path, f]));
}
