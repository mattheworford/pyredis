# PyRedis

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A lite version of a Redis server implemented in Python.

_This project is inspired and guided by ["Write Your Own Redis Server"](https://codingchallenges.fyi/challenges/challenge-redis) from [John Crickett](https://uk.linkedin.com/in/johncrickett)'s
[Coding Challenges](https://codingchallenges.fyi/)._

### Unit Testing
From the root directory, run `python -m pytest`. To run a specific test file, run `python -m pytest <file_name>`.

### Formatting and Linting
Formatting will be automatically done on commit, but to manually format, run `python -m black .`.

### Type Checking
This repository uses [mypy](https://mypy.readthedocs.io/en/stable/index.html) for static type checking. To run mypy, use
the command `python -m mypy . --strict`.
