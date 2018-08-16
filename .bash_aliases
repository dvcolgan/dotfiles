alias l='ls'
alias ll='ls -lX'
alias ..='cd ..;ls'
alias ...='cd ../../;ls'
alias vim='nvim'
alias v='vim'

alias e='. env/bin/activate'

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
alias r='./manage.py runserver [::]:8000'
alias s='./manage.py shell_plus'
alias mm='./manage.py makemigrations'
alias m='./manage.py migrate'
alias gs='git status'
alias gc='git add -A && git commit -m'
alias gp='git push origin master'
