# Project Title

One Paragraph of project description goes here

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

    git clone reponame
    python3 -m virtualenv venv --prompt "project name"
    pip install -r requirements-dev.txt

### Prerequisites

The following software should be installed
- python3
- pip3
- virtualenv

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

    Give the example

And repeat

    until finished

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

Run testing, formatting, and linting by using `nox`.

You can run individual sessions by using the `-s` flag with nox.
For example:

    nox -s test
    nox -s lint

Code is formatted and linted upon commit using the `pre-commit` tool.

Make sure to install the `pre-commit` config using `pre-commit install` once you have installed the `requirements-dev.txt` dependencies.

You can check that everything is passing by running `pre-commit` after `git add`-ing your files to a commit.

> **_NOTE:_** Tests are not run with `pre-commit` due to performance issues, please ensure to run `nox` to validate tests.

## Deployment

Add additional notes about how to deploy this on a live system


## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* Add author names


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
