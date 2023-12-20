# Data Assessment Agent

The data assessment agent is a survey type bot that uses an LLM to re-rank questions after each interaction with a user, thus providing a more interactive experience in surveys.

## Installation instructions

Please make sure to install [Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) first.

```
conda create -n data_assessment_agent python=3.12
conda activate data_assessment_agent
pip install poetry
poetry install
```

## Running Unit Tests

Here it is how you should run unit tests:

```
python -m unittest
```

## Running the server

Please run the server like this from the project's directory:

```
python .\data_assessment_agent\server\assessment_server.py
```