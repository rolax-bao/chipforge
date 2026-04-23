const SAMPLE_VERILOG = `// counter.v — 4-bit up counter with synchronous reset
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
`;

export function EditorPlaceholder() {
  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center gap-2 border-b border-border bg-panel px-3 py-1.5 text-xs text-muted">
        <span className="rounded bg-background px-2 py-0.5 text-foreground">counter.v</span>
      </div>
      <pre className="flex-1 overflow-auto bg-background p-4 font-mono text-sm leading-relaxed text-foreground">
        {SAMPLE_VERILOG}
      </pre>
      <div className="flex items-center justify-between border-t border-border bg-panel px-3 py-1 text-xs text-muted">
        <span>Monaco editor lands in PR #6 · Verilog semantic highlight in PR #6</span>
        <span>UTF-8 · LF · Verilog</span>
      </div>
    </div>
  );
}
