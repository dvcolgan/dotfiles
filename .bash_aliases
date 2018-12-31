alias l='ls'
alias ll='ls -lX'
alias ..='cd ..;ls'
alias ...='cd ../../;ls'
alias vim='nvim'
alias v='vim'

alias e='. `pipenv --venv`/bin/activate'
alias wo='workon $(pwd | rev | cut -d '/' -f 1 | rev)'

alias gogogadget_schemamigration='./manage.py schemamigration --auto'

alias pipupgradeall='pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs pip install -U'

alias wow='git status'
alias such='git'
alias very='git'
alias much='./manage.py'
alias many='./manage.py'

alias t='todo.sh'
complete -F _todo t

alias b='redshift -O 6500'
alias s='./manage.py shell_plus'
alias mm='./manage.py makemigrations'
alias m='./manage.py migrate'

alias rmswp='find . | grep \.swp$ | xargs rm'
alias rmpyc='find . | grep \.pyc$ | xargs rm'

# Thanks to https://gist.github.com/chrisberkhout/210edc1f93882b22900ae11e87d827ce

# git aliases - taken from oh-my-zsh's git plugin and translated to bash
#     https://github.com/robbyrussell/oh-my-zsh/wiki/Cheatsheet#helpful-aliases-for-common-git-tasks
#     https://github.com/robbyrussell/oh-my-zsh/blob/master/plugins/git/git.plugin.zsh

# And then I (David) munged them a little bit
function git_current_branch() {
    ref=$(git symbolic-ref HEAD 2> /dev/null) || \
        ref=$(git rev-parse --short HEAD 2> /dev/null) || return
    echo ${ref#refs/heads/}
}
function git_current_repository() {
    ref=$(git symbolic-ref HEAD 2> /dev/null) || \
        ref=$(git rev-parse --short HEAD 2> /dev/null) || return
    echo $(git remote -v | cut -d':' -f 2)
}
alias g="git"
alias gst="git status"
alias gl="git pull"
alias gup="git pull --rebase"
alias gp="git push"
alias gd="git diff"
alias gdc="git diff --cached"
function gdv() { # mine doesn't add -w
    git diff $@ | vim -R -
}
function gdcv() { # my own
    git diff --cached $@ | vim -R -
}
alias gc="git commit -v"
alias gc!="git commit -v --amend"
alias gca="git commit -v -a"
alias gca!="git commit -v -a --amend"
alias gcmsg="git commit -m"
alias gco="git checkout"
alias gcm="git checkout master"
alias gr="git remote"
alias grv="git remote -v"
alias grmv="git remote rename"
alias grrm="git remote remove"
alias gsetr="git remote set-url"
alias grup="git remote update"
alias gri="git rebase -i"
alias grc="git rebase --continue"
alias gra="git rebase --abort"
alias gb="git branch"
alias gba="git branch -a"
alias gcount="git shortlog -sn"
alias gcl="git config --list"
alias gcp="git cherry-pick"
alias glg="git log --stat --max-count=10"
alias glgg="git log --graph --max-count=10"
alias glgga="git log --graph --decorate --all"
alias glo="git log --oneline --decorate --color"
alias glog="git log --oneline --decorate --color --graph"
alias gss="git status -s"
alias ga="git add"
alias gaa="git add -A"
alias gm="git merge"
alias grh="git reset HEAD"
alias grhh="git reset HEAD --hard"
alias gclean="git reset --hard && git clean -dfx"
alias gwc="git whatchanged -p --abbrev-commit --pretty=medium"
alias gsts="git stash show --text"
alias gsta="git stash"
alias gstp="git stash pop"
alias gstd="git stash drop"
function ggpull {
    git pull origin $(git_current_branch)
}
function ggpur {
    git pull --rebase origin $(git_current_branch)
}
function ggpush {
    git push origin $(git_current_branch)
}
function ggpnp {
    git pull origin $(git_current_branch) && git push origin $(git_current_branch)
}
function glp(){
    git log --pretty=$@
}

alias cdvenv='cd "$WORKON_HOME/$(pwd | rev | cut -d '/' -f 1 | rev)/lib/python2.7/site-packages"'
