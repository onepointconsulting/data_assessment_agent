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

### Installing Postgres

You will need to install Postgres. In Linux you can use this command:

```bash
 sudo apt install postgresql
 sudo apt install libpq-dev
```

And then you will need to access Postgres to run commands in `psql`. You can run the psql tool using as root:

```bash
sudo -u postgres psql template1
```

Make also sure that you change the postgres user's password.

```sql
ALTER USER postgres with encrypted password 'your_password';
```

Make sure that you create your database too with:

```sql
CREATE DATABASE data_assessment_questionnaire
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;
```

The logout from `psql` and access the newly created database with:

```bash
sudo -u postgres psql data_assessment_questionnaire
```

And create all tables with the commands in `sql\db_setup.sql`.


## Running Unit Tests

Here it is how you should run unit tests:

```
python -m unittest
```

## Bootstraping the database

```
python ./data_assessment_agent/bootstrap/import_framework.py
```

## Running the server

Please run the server like this from the project's directory:

```
python ./data_assessment_agent/server/assessment_server.py
```