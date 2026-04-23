/**
 * @chipforge/eda-wasm — browser-side EDA tool wrappers.
 *
 * Placeholder for WASM-based runners. Real integration lands in PR #10 (iverilog)
 * and PR #16 (yosys synthesis). See `docs/architecture.md` §3.3 for the
 * simulation/synthesis flow diagram.
 */

export interface RunResult {
  exitCode: number;
  stdout: string;
  stderr: string;
  /** VCD contents, if the tool produced waveform output. */
  vcd?: Uint8Array;
  durationMs: number;
}

export type EdaTool = 'iverilog' | 'yosys' | 'verilator' | 'verible';

export interface EdaRunner {
  readonly tool: EdaTool;
  run(files: Record<string, string>, args: string[]): Promise<RunResult>;
}

/**
 * Lightweight placeholder runner. Replaced by real YoWASP-backed runners in PR #10.
 * Intentionally exported so packages/ui and apps/web can depend on the shape now.
 */
export class NotImplementedRunner implements EdaRunner {
  constructor(public readonly tool: EdaTool) {}

  async run(_files: Record<string, string>, _args: string[]): Promise<RunResult> {
    return {
      exitCode: 1,
      stdout: '',
      stderr: `${this.tool} WASM runner not yet integrated. Tracked in PR #10 (iverilog) / PR #16 (yosys).`,
      durationMs: 0,
    };
  }
}
