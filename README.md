# PEP Paper Presentation App
*In house application for tracking Paper Presentation Event progress and feedback.*<br>

## To Do:
- Back-end
  - File Rename with upload
  - Testing

- Front-End
  - Main Site Content Upload
  - Dashboard Front-end design 

## How to run?
#### Setting up the Development Environment
For python3 virtual environment:<br>
1. To install python3 virtual environment, refer this:<br>
   ```bash
   pip install virtualenv
   virtualenv --python==python3 pep
   source pep/venv/bin/activate 
   ```
2. The base directory contains 'requirements.txt' file. To replicate the same environment:<br>
   ```bash
   pip install -r requirements.txt
   ```

#### Running for the first time:
1. To migrate databases:<br>
   ```bash
    python manage.py makemigrations [app_name]
    python manage.py migrate
   ```
2. Start the development server:<br>
   ```bash
   python manage.py runserver
   ```
Please file an issue if you face any problem while running the app.<br> 
Improvements are always welcome.<br>
Feel free to fork the repository and send in pull requests with proper commit messages.
