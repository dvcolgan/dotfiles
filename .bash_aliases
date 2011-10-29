alias l='ls'
alias ll='ls -lX'
alias ..='cd ..;ls'
alias ...='cd ../../;ls'
alias v='vim'

alias dev='ssh -p 31415 dcolgan@davidscolgandev.com'
alias fdev='sftp -P 31415 dcolgan@davidscolgandev.com'
alias prod='ssh root@davidscolganprod.com'
alias fprod='sftp root@davidscolganprod.com'
alias dl='cd /cygdrive/c/Users/dcolgan/Downloads'

alias venv='. ~/.virtualenvs/reamplifycrmenv/bin/activate'

clonegithub() {
    git clone git@github.com:dvcolgan/$1.git
}
alias github=clonegithub
