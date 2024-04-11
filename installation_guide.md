# A guide to Weather Australia

## Installation
1. install Python (v3.12, 3.11 should work too)
2. clone main branch locally
3. set up vscode venv (see venv_guide.md)
4. run `pip install -r requirements.txt` to install all dependencies in venv
5. for all terminal commands, make sure your working directory is `/Code/`

## Running the app
- initialize the database (only has to be done once): run `flask --app weatherApp init-db`
- to run the app, use `flask --app weatherApp --debug run` and follow the link

## Running tests
- see testing_guide.md