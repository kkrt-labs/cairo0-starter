# Cairo0 Starter

A set of exercises forked from [Starklings](https://github.com/onlydustxyz/starklings) to get you started with Cairo0.

## Installation

The project uses python 3.10. The recommended way to install it if you don't have it yet is to use [uv](https://docs.astral.sh/uv/getting-started/installation/).

Once installed, install the required dependencies by running the following command:

```bash
uv sync
```

## Exercises

Exercises are located in the `exercises` directory. Each exercise has a corresponding test file with the same name in python,
that verifies the correctness of the implementation.

## Tests

To test your implementation of an exercise, run the following command:

```bash
uv run pytest path/to/exercise.py
```

To test all exercises, run the following command:

```bash
uv run pytest exercises
```

## References

- [Starklings](https://github.com/onlydustxyz/starklings)
- [Cairo0 Documentation](https://docs.cairo-lang.org/cairozero/hello_cairo/index.html)
- [Cairo Whitepaper](https://eprint.iacr.org/2021/1063.pdf)


## LSP & IDE Setup

To enhance your development experience in VSCode, we recommend installing the following extensions:

- **[Cairo by StarkWare Industries](https://marketplace.cursorapi.com/items?itemName=Starkware.cairo)** (ensure it’s the first version, not the new Cairo 1.0)
- **[Cairo Language Support for StarkNet by Eric Lau](https://marketplace.cursorapi.com/items?itemName=ericglau.cairo-ls)**

These extensions provide Language Server Protocol (LSP) support, enabling features like autocompletion, syntax highlighting, and module navigation.

### Activating the LSP

After installing the extensions, follow these steps to set up your environment:

1. Open a terminal and navigate to the `cairo0-starter` directory:
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
