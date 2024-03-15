## Git Tips
- For all this stuff, you have to be in the folder of your repo

### Getting stuff from remote repo
- `git clone <clone-url>` - Create a local version of a remote repo: 
- `git pull` - Make sure your repo is up to date: 

### Making changes
- `git add .` - stage changes
- `git commit -m"<commit-message>"` - commit changes
- `git commit -m"<commit-message>" -m"<commit-message-details>` - commit changes with a more detailed description
- `git status` - see summary of all changes
- `git push` - push changes to remote repo

### Branching
- `git checkout -b <branch-name>` - Create and switch to a new branch (off of main , by default)
- `git checkout -b <sub-branch-name> <existing-branch>` - Create and switch to a new branch (off of a branch other than main)
- `git push -u origin <branch-name>` - Push a newly created local branch to the remote repository[^1] 
- `git switch <branch-name>` - Switch to branch "branch-name"
- `git push -d origin <branch-name>` - Delete branch remotely (make sure you're not on that branch)
- `git branch -d <branch-name>` - Delete branch locally

[^1]: You don't have to do this if you change your git configuration with `git config --global --add --bool push.autoSetupRemote true`. This will let you just run `git push` every time.


