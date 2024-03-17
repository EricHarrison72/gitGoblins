# Testing Guide

General guidelines as stated in our test plan (milestone 3):
- One class/module ⇒ one test file. 
- One function/action ⇒ one unit test
- Aim for full coverage; give tests data that covers all decision branches

For most terminal commands below, your cwd should be the `Code` folder.

## Python Unit Tests
#### In the terminal:
- `pytest` will run all Python unit tests
- `pytest test_file.py` runs a specific test file

#### Using VS Code:
- On the testing tab (probably on left of your screen, it looks like a chemistry flask), you can configure your unit testing settings
- This might already be configured for you since `.vscode/settings.json` was pushed to GitHub
- This provides a nice UI for your to easily run and debug specific tests

## JS Unit Tests
#### Set-up:
- You will have to [download Node.js](https://nodejs.org/en/download) in order to use `npm`. Then restart VS Code.
- Install the JS testing framework _Jest_ by running the terminal command `npm install jest`
- make sure to add a `.gitignore` file (with the contents "`*`") to the huge `node_modules` folder that will generate in your local repo

#### In the terminal:
- `npm test` will run all JS unit tests

#### Using VS Code
- Install the [Jest extension](https://marketplace.visualstudio.com/items?itemName=Orta.vscode-jest)
- You should be able to access/configure Jest in the same testing tab as Python unit tests.

## See Your Coverage (Python only)
#### To visualize coverage in editor:
- Install the VS Code extension [Coverage Gutters](https://marketplace.visualstudio.com/items?itemName=ryanluker.vscode-coverage-gutters) (ryanluker.vscode-coverage-gutters)

1. In terminal, run your unit tests: `coverage run -m pytest`
2. In terminal, Generate a .xml report: `coverage xml`
3. Click on the `Watch` button (in the bottom left corner of your editor)
4. If you open one of the tested files (e.g. `auth.py`), you should see coloured highlights that indicate which lines of code are (or aren't) covered by the unit tests.
5. Click on the same button (it now says `X% Coverage`) to disable coverage view

#### Alternative Options:
1. Run your unit tests: `coverage run -m pytest`
2. Output a report with one of the following options:
   - `coverage report` outputs a very simple report in the terminal
   - `coverage html` generates an interactive version of the report which you can open in a browser

#### Checking Coverage Before Merging
- There is a GitHub Actions workflow that automatically generates a basic coverage report and comments it on new pull requests. 
- If you are reviewing code, be sure to look at this report.

## Integration Testing
We have two GitHub Actions workflows (CI and JS CI) that make unit testing part of our continuous integration pipeline. 

These workflows run automatically on every push and pull request. They install dependencies, build the program, and run all unit tests on several virtual machines, so that we can test the program on different operating systems (latest releases of Ubuntu, Windows, MacOS), as well as a few different versions of Python (currently 3.11 and 3.12). 

Essentially, the CI and JS CI workflows catch little errors that we might not if we simply ran tests on our own machines, and ensure that new code does not break old tests. **You don't have to do anything except check the test report on GitHub if the tests fail.**
