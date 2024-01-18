# PyRedis

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Tests Status](./tests-badge.svg)](./reports/junit/report.html)

A lite version of a Redis server implemented in Python.

_This project is inspired and guided by ["Write Your Own Redis Server"](https://codingchallenges.fyi/challenges/challenge-redis) from [John Crickett](https://uk.linkedin.com/in/johncrickett)'s
[Coding Challenges](https://codingchallenges.fyi/)._

This project provides a lite version of a Redis server that can handle a subset of Redis commands and responses.

### Features

This implementation supports the following commands:

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

It also uses the Redis Serialization Protocol (RESP) as its protocol for communication between client and server.

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
pip install -r requirements.txt
```

### Usage

To start the Redis server, run the following command:

```bash
$ python -m pyredis
```

This will start the server on port 6379.

To use the CLI client, run the following command:

```bash
$ python -m cli.py
```
This will start the client and connect to the Redis clone server running on
localhost:6379
.

### Testing

To run tests for the project, navigate to the root folder and run the following command:

```bash
pytest
```
This will run all tests in the /tests/ directory.

### Contributing
If you find any issues with the project or would like to suggest improvements, feel free to create a pull request on the project's GitHub repository.

### License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### What I Learned
This project helped me learn and apply the following concepts:

* Test-driven development - writing test cases before writing production code
* Network programming - understanding how client-server communication works over a network
* Continuous integration - using GitHub Actions to enable continuous integration of the project's test suite
* Concurrency - using Python's threading module to handle multiple client connections concurrently
* Performance optimization - improving the implementation of certain commands such as LRANGE for better performance.
* Overall, this project was a great learning experience in creating a functioning server and client, understanding Redis commands and protocol, and building a project from the ground up using best practices.