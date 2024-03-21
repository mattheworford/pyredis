# PyRedis

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Tests Status](./tests-badge.svg)](./reports/junit/report.html)

PyRedis provides a lite version of a Redis server, implemented in Python, that can handle a subset of Redis commands and responses.

## Getting Started

### Prerequisites

- [Python](https://www.python.org/downloads/) installed on your machine.

### Installation

To install, follow the steps below:

Clone the repository to your local machine:

```bash
git clone https://github.com/mattheworford/pyredis.git
```

Change directory to the project folder:

```bash
cd pyredis
```

Install the required dependencies:

```bash
pip3 install -r requirements.txt
```

### Usage

To start the Redis server, run the following command:

```bash
$ python3 -m pyredis
```

This will start the server on port 6379.

To use the CLI client, run the following command:

```bash
$ python3 -m cli.py
```

This will start the client and connect to the Redis clone server running on `localhost:6379`.

_Note: You can also use the original [Redis CLI](https://redis.io/docs/connect/cli/) with a PyRedis server or vice versa._

### Testing

To run tests for the project, navigate to the root folder and run the following command:

```bash
pytest
```
This will run all tests in the `tests` directory.

## Features

This project supports the following commands:

* `PING`
* `ECHO`
* `SET`
* `GET`
* `EXISTS`
* `INCR`
* `DECR`
* `LPUSH`
* `RPUSH`
* `LRANGE`
* `DEL`

It uses the [Redis Serialization Protocol](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiEzsCP1OiDAxUwlGoFHWZoDQoQFnoECAcQAQ&url=https%3A%2F%2Fredis.io%2Fdocs%2Freference%2Fprotocol-spec%2F&usg=AOvVaw1WbAZfA9lYyJe7McNlJmJb&opi=89978449) (RESP) as its protocol for communication between client and server.

## Learnings

This project helped me learn and apply the following concepts:

* Test-driven development - writing test cases before writing production code
* Network programming - understanding how client-server communication works over a network
* Continuous integration - using GitHub Actions to enable continuous integration of the project's linting, type checking and test suite
* Concurrency - using Python's [asyncio](https://docs.python.org/3/library/asyncio.html) library to handle multiple client connections concurrently
* Performance optimization - improving the implementation of certain commands such as `LRANGE` for better performance

Overall, this project was a great learning experience in creating a functioning server and client, understanding Redis commands and protocol, and building a project from the ground up using various development best practices.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- This project is inspired and guided by ["Write Your Own Redis Server"](https://codingchallenges.fyi/challenges/challenge-redis) from [John Crickett](https://uk.linkedin.com/in/johncrickett)'s
[Coding Challenges](https://codingchallenges.fyi/).
