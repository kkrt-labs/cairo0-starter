# Cairo0 Starter 🐫❤️

Welcome to Cairo0 Starter, a tool to help you learn Cairo 0 through small exercises. This tool is modeled after the popular [Rustlings](https://github.com/rust-lang/rustlings) project, but for Cairo 0, and inspired from [Starklings](https://github.com/onlydustxyz/starklings).

## Getting Started

### Prerequisites

- Python 3.10
- [uv](https://docs.astral.sh/uv/getting-started/installation/). (Python package manager)

### Installation

1. Clone this repository:
   ```bash
   cd /path/to/cairo0-starter
   ```
2. Synchronize dependencies using `uv` (skip this if already done):
   ```bash
   uv sync
   ```
3. Activate the local Python virtual environment (required for `cairo-compile` to be available in locally):
   ```bash
   source ./.venv/bin/activate
   ```
4. Launch your IDE from the terminal with the Python environment active:
   ```bash
   code .    # For VSCode
   cursor .  # For Cursor
   ```

## Usage

### Watch Mode

The watch mode is the recommended way to work through the exercises. It will monitor your files for changes and automatically run tests when you modify an exercise file:

```bash
uv run cairo0-rustlings watch
```

In watch mode, you can use the following commands:

- `h`: Show a hint for the current exercise
- `r`: Manually run the test for the current exercise
- `l`: Show a list of all exercises
- `q`: Quit watch mode
- `Ctrl+C`: Exit the program

### Exercise List

To see a list of all exercises and their status:

```bash
uv run cairo0-rustlings list
```

In the exercise list, you can:

- Navigate exercises with `p` (previous) and `n` (next)
- Continue a selected exercise with `c`
- Reset an exercise's status with `r`
- Return to watch mode with `q`

## How to Complete Exercises

Each exercise consists of:

1. A Cairo file (`.cairo`) containing the exercise
2. A Python test file (`.py`) containing the test case

To mark an exercise as complete:

1. Edit the Cairo file to solve the exercise
2. Remove the `// I AM NOT DONE` comment line
3. Save the file
4. The watch mode will automatically run the test to check your solution

### References

- [Starklings](https://github.com/onlydustxyz/starklings)
- [Cairo0 Documentation](https://docs.cairo-lang.org/cairozero/hello_cairo/index.html)
- [Cairo Whitepaper](https://eprint.iacr.org/2021/1063.pdf)

## LSP & IDE Setup

To enhance your development experience in VSCode, we recommend installing the following extensions:

- **[Cairo by StarkWare Industries](https://marketplace.cursorapi.com/items?itemName=Starkware.cairo)** (ensure it’s the first version, not the new Cairo 1.0)
- **[Cairo Language Support for StarkNet by Eric Lau](https://marketplace.cursorapi.com/items?itemName=ericglau.cairo-ls)**

These extensions provide Language Server Protocol (LSP) support, enabling features like autocompletion, syntax highlighting, and module navigation.
