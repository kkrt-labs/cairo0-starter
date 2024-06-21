# Cairo0 Starter

A set of exercises forked from [Starklings](https://github.com/onlydustxyz/starklings) to get you started with Cairo0.

## Installation

The project uses python 3.10. The recommended way to install it if you don't have it yet is to use [pyenv](https://github.com/pyenv/pyenv).

```bash
pyenv install 3.10
```

Install the required dependencies by running the following command:

```bash
poetry install
```

## Exercises

Exercises are located in the `exercises` directory. Each exercise has a corresponding test file with the same name in python,
that verifies the correctness of the implementation.

## Tests

To test your implementation of an exercise, run the following command:

```bash
poetry run pytest path/to/exercise.py
```

To test all exercises, run the following command:

```bash
poetry run pytest exercises
```
