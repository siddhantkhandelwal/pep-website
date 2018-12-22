# Paper Presentation Portal

Built for Paper Evaluation and Presentation Event, APOGEE 2019.
[Live!](https://bits-apogee.org/paper-presentation/admin/)

## Development

- Django
- SQL
- Nginx Server (Thanks, Department of Visual Media)

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
