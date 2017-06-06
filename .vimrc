set nocompatible
filetype off

set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

Plugin 'VundleVim/Vundle.vim'
Plugin 'ap/vim-css-color' 
"Plugin 'jeroenbourgois/vim-actionscript' 
"Plugin 'groenewege/vim-less'
"Plugin 'nielsmadan/harlequin'
"Plugin 'vim-scripts/pyte'
"Plugin 'kchmck/vim-coffee-script'
Plugin 'pangloss/vim-javascript'
"Plugin 'mxw/vim-jsx'

"Plugin 'jelera/vim-javascript-syntax'
Plugin 'kien/ctrlp.vim'
Plugin 'nanotech/jellybeans.vim'
Plugin 'reedes/vim-colors-pencil'
"Plugin 'jdonaldson/vaxe'
"Plugin 'digitaltoad/vim-jade'
"Plugin 'altercation/vim-colors-solarized'
Plugin 'scrooloose/syntastic'
"Plugin 'mklabs/grunt.vim'
"Plugin 'lambdatoast/elm.vim'
Plugin 'janko-m/vim-test'
"Plugin 'rust-lang/rust.vim'
"Plugin 'wavded/vim-stylus'
Plugin 'posva/vim-vue'
Plugin 'plasticboy/vim-markdown'
Plugin 'leafgarland/typescript-vim'
Plugin 'Quramy/tsuquyomi'
Plugin 'Shougo/vimproc.vim'
"Plugin 'clausreinke/typescript-tools.vim'
"Plugin 'Valloric/YouCompleteMe'
Plugin 'SirVer/ultisnips'
"Plugin 'davidhalter/jedi-vim'
Plugin 'hynek/vim-python-pep8-indent'
Plugin 'dracula/vim'
Plugin 'mattn/emmet-vim'
"Plugin 'briancollins/vim-jst'
"Plugin 'flowtype/vim-flow'
"Plugin 'w0rp/ale'

au BufRead,BufNewFile *.ts  setlocal filetype=typescript
let g:vim_markdown_fenced_languages = ['python=python', 'bash=sh']
let g:vim_markdown_folding_disabled = 1
call vundle#end()
filetype plugin indent on
syntax on

let g:ale_lint_on_save = 1
let g:ale_lint_on_text_changed = 0

let g:tsuquyomi_disable_quickfix = 1
let g:syntastic_typescript_checkers = ['tsuquyomi']
let g:tsuquyomi_completion_detail = 1

let g:UltiSnipsExpandTrigger="<tab>"
let g:UltiSnipsExpandTrigger="<c-x><c-k>"

"let g:syntastic_python_checkers = ['flake8']

let g:javascript_plugin_flow = 1
let g:jsx_ext_required = 0
"let g:syntastic_javascript_checkers = ['eslint', 'flow']
"let g:syntastic_javascript_flow_exe = 'flow'
"let g:syntastic_javascript_eslint_exec = 'eslint_d'
let g:ale_linters = {
\   'javascript': ['eslint']
\}
let g:flow#enable = 0

"set statusline+=%#warningmsg#
"set statusline+=%{SyntasticStatuslineFlag()}
"set statusline+=%*
"
"
"let g:syntastic_vue_checkers = ['eslint']
"let g:syntastic_vue_eslint_exec = 'eslint_d'
autocmd BufRead,BufNewFile *.vue setlocal filetype=vue.html.javascript.css


let mapleader = ","
set nocompatible " Vim rather than Vi
set t_Co=256 " force 256 colors in terminal

set linebreak

" APPEARANCE
set textwidth=0
set hidden
set ruler
set showmode		                " display curent mode
set showcmd		                    " display incomplete commands
set number			                    " show line numbers
set ignorecase

" DEFAULT TAB STOPS & INDENTING
set tabstop=4		                " tab stops
set softtabstop=4
set shiftwidth=4	                " number of spaces to use for each step of (auto)indent
set autowriteall
set nowritebackup

set shiftround                      " Round indents to multiples of shiftwidth

set expandtab
set smarttab

set backspace=2
set showmatch
set pastetoggle=<F12>

set history=200
set undolevels=200
"set ttyfast		                    " smoother output, they claim
set whichwrap=h,l,~,[,]

set incsearch
set noerrorbells
set hlsearch

"nnoremap / /\v
"cnoremap %s/ %s/\v

nnoremap <C-e> 3<C-e>
nnoremap <C-y> 3<C-y>
no <space><space> :wa<cr>:w<cr>
no <leader>d !!date +"\%A \%B \%d, \%Y \%r"<cr>
no <leader>D !!date +"\%B \%d, \%Y"<cr>
no <leader>v :vsp $MYVIMRC<cr>
no <leader>s :source $MYVIMRC<cr>
"no <leader>u :!./manage.py test intake --nomigrations<cr>
no <leader>u :!npm test<cr>

"no <leader>n :cnext<cr>
"no <leader>p :cprevious<cr>

ino # X#

no <leader>h :nohl<cr>

no  zz
no t gj
no n gk
no s l
no l n
no j t
no k s

no T }
no N {
no L N
no J T
no K S
no S $
no H ^

no - J

no Q gqap

no h h
no t j
no n k
no s l


ino <C-c> <esc>
    no <SPACE> <C-w>
    no <SPACE>h <C-w>h
    no <SPACE>t <C-w>j
    no <SPACE>n <C-w>k
    no <SPACE>s <C-w>l

imap <F4> {}<UP>zzo
imap <F5> {}<UP>zzo
imap <F6> {});<UP>zzo

let g:ctrlp_custom_ignore = 'node_modules\|DS_Store\|git'

" TECHNICAL
set mouse=a
set encoding=utf-8
set fileencoding=utf-8
set termencoding=utf-8

set autoindent
set smartindent
au Filetype yaml setlocal tabstop=2 softtabstop=2 shiftwidth=2
au filetype elm call DisableIndent()

function! DisableIndent()
    set autoindent&
    set cindent&
    set indentexpr&
endfunction


iab lorem Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
iab helo hello
iab teh the
iab tommorrow tomorrow

"function! Reload()
"    execute ':silent !/home/dcolgan/projects/conferam/reload.sh'
"    execute ':redraw!'
"endfunction
"autocmd BufWritePost *.py call Reload()

set guioptions+=mTLlRrb
set guioptions-=mTLlRrb

let g:omni_sql_no_default_maps = 1

set term=xterm-256color
iab pdb import ipdb; ipdb.set_trace()
iab rdb ((val: any) => { console.log(val); return val; })(

iab rcc class extends Component {render() {return ();}};

"nnoremap <leader>el :ElmEvalLine<CR>
"vnoremap <leader>es :<C-u>ElmEvalSelection<CR>
"nnoremap <leader>em :ElmMakeCurrentFile<CR>
no <space>l :!love .<cr>

nnoremap <space>r :let _s=@/<Bar>:%s/\s\+$//e<Bar>:let @/=_s<Bar><CR>

"let test#python#runner = 'djangotest'
no <leader>t :TestNearest -k -n<cr>
no <leader>T :TestNearest<cr>
no <leader>t :!npm test<cr>

"no <leader>t :!npm test<cr>
"no <leader>t :!lime test neko<cr>


inoremap {<cr> {<cr>}<c-o>O
inoremap {,<cr> {<cr>},<c-o>O
inoremap {;<cr> {<cr>};<c-o>O
inoremap {)<cr> {<cr>})<c-o>O
inoremap {{<cr> {<cr>});<c-o>O

"colorscheme pencil
"set bg=light
set bg=dark
colorscheme jellybeans

set directory=~/.vim/swap,.
au BufNewFile,BufFilePre,BufRead *.md set filetype=markdown
"let &statusline .= ' %{ line2byte(line("$")+1)-1 }C'
"set laststatus=2

no <leader>b :.w! /home/dvcolgan/.current-task<cr>
no <leader>e ddGp^d0<c-o>zz
no <leader>B :!date -Iseconds > ~/.start-time<cr>
no <leader>E :!/home/dvcolgan/bin/end-session<cr>
no <leader>R :!rm /home/dvcolgan/.sessions-today && touch /home/dvcolgan/.sessions-today<cr>
