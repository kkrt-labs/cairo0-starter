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
- [Cairo0 Documentation](https://www.cairo-lang.org/docs/hello_cairo.html)
- [Cairo Whitepaper](https://eprint.iacr.org/2021/1063.pdf)
