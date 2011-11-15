alias l='ls'
alias ll='ls -lX'
alias ..='cd ..;ls'
alias ...='cd ../../;ls'
alias v='vim'

alias harp='cd ~/projects/harp/; . bin/activate; cd harp'

alias dsc='ssh davidsc4@davidscolgan.com'
alias fdsc='sftp davidsc4@davidscolgan.com'

alias dev='ssh -p 31415 dcolgan@davidscolgandev.com'
alias fdev='sftp -P 31415 dcolgan@davidscolgandev.com'
alias dl='cd /cygdrive/c/Users/dcolgan/Downloads'
alias john='ssh john.cse.taylor.edu'
alias fjohn='sftp john.cse.taylor.edu'
alias matt='ssh matthew.cse.taylor.edu'
alias fmatt='sftp matthew.cse.taylor.edu'

function workonfn {
    . ~/virtualenvs/$1/bin/activate
    cd ~/projects/$1
}

alias workon='workonfn'
