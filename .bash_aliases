alias l='ls'
alias ll='ls -lX'
alias ..='cd ..;ls'
alias ...='cd ../../;ls'
alias v='vim'

alias dev='ssh -p 31415 dcolgan@davidscolgandev.com'
alias fdev='sftp -P 31415 dcolgan@davidscolgandev.com'
alias prod='ssh root@davidscolganprod.com'
alias fprod='sftp root@davidscolganprod.com'

alias dsc='ssh davidsc4@davidscolgan.com'
alias fdsc='sftp davidsc4@davidscolgan.com'

alias dl='cd /cygdrive/c/Users/dcolgan/Downloads'
alias john='ssh john.cse.taylor.edu'
alias fjohn='sftp john.cse.taylor.edu'
alias matt='ssh matthew.cse.taylor.edu'
alias fmatt='sftp matthew.cse.taylor.edu'
alias harp='ssh harp@john.cse.taylor.edu'
alias fharp='sftp harp@john.cse.taylor.edu'

function workonfn {
    . ~/projects/$1env/bin/activate
    cd ~/projects/$1
}
alias workon='workonfn'

function punchfn {
    git add .
    git commit -m "$1"
    git push origin master
}

alias punch='punchfn'

alias in='cygstart.exe -- /cygdrive/c/Users/dcolgan/Desktop//setup.exe -K http://cygwinports.org/ports.gpg'
