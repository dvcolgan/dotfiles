alias l='ls'
alias ll='ls -lX'
alias ..='cd ..;ls'
alias ...='cd ../../;ls'
alias v='vim'

alias dev='ssh -p 337 dcolgan@davidscolgandev.com'
alias fdev='sftp -P 337 dcolgan@davidscolgandev.com'
alias dl='cd /cygdrive/c/Users/dcolgan/Downloads'

clonegithub() {
    git clone git@github.com:dvcolgan/$1.git
}
alias github=clonegithub

