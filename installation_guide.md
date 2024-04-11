# A guide to Thunder Down Under
_Please note: for all terminal commands, make sure your current working directory is the `/Code/` folder._

## Installation and Setup
### Set up the project on your machine
We used VS Code to develop our project; we recommend you do the same to run it (at least if you want to follow this guide)

1. **Install Python.** Make sure you have [Python 3.12](https://www.python.org/downloads/) installed (3.11 should work too). 
2. **Clone this repository locally.**
Put it where ever you want. Presumably the person looking at this knows how to do this.
3. **Set up a virtual environment**.
    - In VS Code, open the Command Palette (**View** > **Command Palette** or (`Ctrl+Shift+P`)). 
    - Then select the **Python: Create Environment** command to create a virtual environment in your workspace. Select **Venv** and then the Python environment you want to use to create it.
      - The first time you do this, you will have to tell it where to look for your Python installation. Ian's was in `~/appdata/programs/python/python312/python.exe`

### Install the project requirements
- in the terminal, run `pip install -r requirements.txt` to install all dependencies in the venv

## Running the app

- Initialize the database and prediction model by running `flask --app weatherApp init-db` in the terminal (you should only have to do this once)
- To run the app, run the command `flask --app weatherApp --debug run` and follow the link that appears in the terminal.

### Logging in
- Your email will only be stored on your local instance of the database; we will not have access to it. But if you don't want to use your personal email, try using a [temp-mail](https://temp-mail.org/en/).

## Running tests
- see our internal testing documentation in the file `~/Code/tests/testing_guide.md`.

## Project Organization
An overview of the files structure that will help you find the important stuff (doesn't contain everything).
```
gitGoblins/
  |-- .github/workflows/
  |     |-- [YAML files for testing automation]
  |
  |-- Code/
  |     |-- data/weatherAUS.csv [dataset that populates db]
  |     |-- instance/ [contains actual db]
  |     |-- node_modules/
  |     |-- tests/
  |     |     |-- testing_guide.md
  |     |     |-- [python tests]
  |     |     |-- [js tests]
  |     |
  |     |-- weatherApp/ [the actual app itself]
  |           |-- static/
  |           |     |-- css/
  |           |     |-- img/
  |           |     |-- js/
  |           |-- templates/ 
  |           |     |-- [html.jinja templates]
  |           |-- [python backend logic]
  |           |-- schema.sql
  |
  |-- Database_Design/
  |-- Exploration_and_Research/
  |-- Milestones/
  |-- Requirements/
  |-- Scrum_Meetings/
  |-- .gitignore
  |-- installation_guide.md
  |-- team_agreement.md
```
