# Improve a Django Project
This is the project 9 for the Python Web Development Techdegree program.

The purpose of this project was to clean up and improve a simple existing project
that had some significant problems. Among them:

- Incorrect field types on models
- Incompatible dependencies in requirements
- Broken and redundant templates
- Poorly implemented queries that heavily impacted performance


## Installation

1. Download the project and change into the project directory.
2. Create a new virtual environment 
    - Windows: `python -m venv env` 
    - Linux/Mac `python3 -m venv env`
3. Activate the virtual environment
    - Windows: `.\env\Scripts\activate`
    - Linux/Mac: `source env/bin/activate`
4. `pip install -r requirements.txt` to install the project dependencies.
   - Required JavaScript files are included with the download. 
5. `python manage.py runserver` to start the server on port 8000 (default).
6. Open [127.0.0.1:8000](127.0.0.1:8000) in your browser.

Note: Normal users likely wouldn't need to log in, so there is no login link
on the front page. If you want to create new menus or edit entries, 
you can log in by going to [127.0.0.1:8000/login/](127.0.0.1:8000/login/).

A test user has been created with the following credentials:

username: `testuser`

password: `test`