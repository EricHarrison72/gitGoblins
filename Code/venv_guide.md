# Venv Guide
Every time you are working on the project, you have to make sure you have the most current packages installed in your virtual environment (or "venv"). *Venvs don't get pushed to the repository.* Instead, a requirements.txt file contains all you need to quickly duplicate the venv of your teammates.

### Setting up a virtual environment:
1. In VS Code, open the Command Palette (**View** > **Command Palette** or (`Ctrl+Shift+P`)). Then select the **Python: Create Environment** command to create a virtual environment in your workspace. Select **Venv** and then the Python environment you want to use to create it.
    - The first time you do this, you will have to tell it where to look for the Python installation. Ian's was in `~/appdata/programs/python/python312/python.exe`
2. After your virtual environment creation has been completed, run **Terminal: Create New Terminal** (`` Ctrl+Shift+` ``) from the Command Palette, which creates a terminal and automatically activates the virtual environment by running its activation script.

### Making sure your venv is up-to-date
1. In the VS Code terminal, run the command `pip install -r requirements.txt`. This will automatically install all the dependencies used by other project members on your virtual environment. 

### Making changes to the venv
1. If you are the first person to use a new tool/package, you will run a command like `pip install flask` in the VS Code terminal. In this case, others will need to install it in their venv as well. So before you push: 
2. Delete the current requirements.txt file. 
3. In the VS Code terminal, run the command `pip freeze > requirements.txt`.

These steps also apply if you decide to remove a dependency - but be extra careful with that; we don't want code breaking just because some silly billy decided we're not using a specific tool anymore. 

