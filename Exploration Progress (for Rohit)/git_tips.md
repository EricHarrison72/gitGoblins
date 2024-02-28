## Git Tips
- For all this stuff, you have to be in the folder of your repo

### Getting stuff from remote repo
- `git clone <clone-url>` - Create a local version of a remote repo: 
- `git pull` - Make sure your repo is up to date: 

### Making changes
- `git add .` - stage changes
- `git commit -m"<commit-message>"` - commit changes
- `git push` - push changes to remote repo

### Branching
- `git checkout -b <branch-name>` - Create and switch to a new branch 
- `git switch <branch-name>` - Switch to branch "branch-name"
- `git push -u origin <branch-name>` - Push a newly created local branch to the remote repository
- `git push -d origin <branch-name>` - Delete branch remotely (make sure you're not on that branch)
- `git -d <branch-name>` - Delete branch locally


