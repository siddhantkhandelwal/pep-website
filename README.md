# Paper Presentation Portal

- Built for Paper Evaluation and Presentation Event, APOGEE 2019.
- Description on [blog post](https://siddhantkhandelwal.github.io/paper-presentation-portal/)

### Setting up the Development Environment

- Virtual Environment setup:

```bash
pip install virtualenv
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

- Migrating databases:

```bash
python manage.py makemigrations
python manage.py migrate
```

- Start the local server:

```bash
python manage.py runserver
```
