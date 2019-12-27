set nocompatible
filetype off

set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

Plugin 'VundleVim/Vundle.vim'
"Plugin 'vimwiki/vimwiki'

" Colors
Plugin 'dracula/vim'
Plugin 'mightwork/summerfruit256.vim'
Plugin 'nanotech/jellybeans.vim'


" IDE things
Plugin 'kien/ctrlp.vim'
Plugin 'scrooloose/nerdtree'
Plugin 'janko-m/vim-test'
Plugin 'w0rp/ale'
Plugin 'tpope/vim-markdown'

" Javascript
Plugin 'posva/vim-vue'

Plugin 'pangloss/vim-javascript'
Plugin 'maxmellon/vim-jsx-pretty'

" Python
Plugin 'hynek/vim-python-pep8-indent'
Plugin 'niftylettuce/vim-jinja'

call vundle#end()
filetype plugin indent on
syntax on

let g:ale_virtualenv_dir_names = []
let g:python_flake8_use_global = 1

let g:ctrlp_follow_symlinks = 1
let g:ctrlp_custom_ignore = '\v[\/](output|env|dist|staticfiles|node_modules|__pycache__|deps|_build)|(\.(swp|git|png|jpg|pyc))$'

autocmd BufRead,BufNewFile *.mjs setlocal filetype=javascript

highlight nonascii guibg=Red ctermbg=1 term=standout
au BufReadPost * syntax match nonascii "[^\u0000-\u007F]"

let mapleader = ","
set nocompatible " Vim rather than Vi
set termguicolors
set linebreak
set textwidth=0
set hidden
set ruler
set showmode
set showcmd
set number
set ignorecase
set tabstop=4
set softtabstop=4
set shiftwidth=4
set autowriteall
set nowritebackup
set backupcopy=yes
set shiftround
set expandtab
set smarttab
set backspace=2
set showmatch
set history=200
set undolevels=200
set whichwrap=h,l,~,[,]
set incsearch
set noerrorbells
set hlsearch
nnoremap <C-e> 3<C-e>
nnoremap <C-y> 3<C-y>
no <space><space> :wa<cr>:w<cr>
no <leader>D !!date +"\%A \%B \%d, \%Y \%r"<cr>
no <leader>d !!date +"\%B \%d, \%Y"<cr>
no <leader>d !!date +"\%B \%d, \%Y"<cr>
no <leader>v :vsp $MYVIMRC<cr>
no <leader>s :source $MYVIMRC<cr>
no <leader>u :!npm test<cr>
ino # X#
no <leader>h :nohl<cr>

" Wiki
let g:vimwiki_list = [{'path': '~/vimwiki/', 'syntax': 'markdown', 'ext': '.md'}]


" Make Dvorak nicer and fix the hjkl offset by one
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

" I heart this mapping
no - J
no Q gqap
no h h
no t j
no n k
no s l
no <leader>nn :NERDTree<cr>
no <leader>nf :NERDTreeFind<cr>
vnoremap y "*y

let g:NERDTreeMapOpenInTab = ''
let NERDTreeIgnore = ['\.pyc$']

ino <C-c> <esc>
no <SPACE> <C-w>
no <SPACE>h <C-w>h
no <SPACE>t <C-w>j
no <SPACE>n <C-w>k
no <SPACE>s <C-w>l

imap <F4> {}<UP>zzo
imap <F5> {}<UP>zzo
imap <F6> {});<UP>zzo

" TECHNICAL
set mouse=a
set encoding=utf-8
set fileencoding=utf-8
set termencoding=utf-8
set autoindent
set smartindent
au Filetype markdown setlocal tabstop=4 softtabstop=4 shiftwidth=4
au Filetype yaml setlocal tabstop=2 softtabstop=2 shiftwidth=2
autocmd FileType markdown,text setlocal spell

iab lorem Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
iab helo hello
iab teh the
iab tommorrow tomorrow
iab yuor your

set guioptions+=mTLlRrb
set guioptions-=mTLlRrb

set pastetoggle=<F12>

let g:omni_sql_no_default_maps = 1

iab pdb import ipdb; ipdb.set_trace()
iab rdb ((val: any) => { console.log(val); return val; })(

inoremap {<cr> {<cr>}<c-o>O
inoremap {,<cr> {<cr>},<c-o>O
inoremap {;<cr> {<cr>};<c-o>O
inoremap {)<cr> {<cr>})<c-o>O
inoremap {{<cr> {<cr>});<c-o>O

colorscheme summerfruit256
set bg=light
"set bg=dark
"colorscheme jellybeans

no <leader>cd :colorscheme jellybeans<cr>:set bg=dark<cr>
no <leader>cl :colorscheme summerfruit256<cr>:set bg=light<cr>

au BufNewFile,BufFilePre,BufRead *.md set filetype=markdown
"let &statusline .= ' %{ line2byte(line("$")+1)-1 }C'
"set laststatus=2

" Fix syntax highlighting breaking in vue files among others
"autocmd BufEnter *.vue :syntax sync fromstart
autocmd BufEnter *.html :syntax sync fromstart
autocmd BufEnter *.md :syntax sync fromstart

" vim-test
nmap <silent> <leader>tN :TestNearest<CR>
nmap <silent> <leader>tF :TestFile<CR>
nmap <silent> <leader>tS :TestSuite<CR>
nmap <silent> <leader>tL :TestLast<CR>
nmap <silent> <leader>tV :TestVisit<CR>

nmap <silent> <leader>tn :TestNearest<CR>
nmap <silent> <leader>tf :TestFile<CR>
nmap <silent> <leader>ts :TestSuite<CR>
nmap <silent> <leader>tl :TestLast<CR>
nmap <silent> <leader>tv :TestVisit<CR>


let test#strategy = "neovim"
let test#python#pytest#options = '--capture=no'
"let test#python#runner = 'pytest'
let test#javascript#runner = 'jest'
let test#javascript#jest#file_pattern = '\v(tests/test_.*)\.(js|jsx|coffee|ts|tsx)$'

autocmd BufRead,BufNewFile /home/dvcolgan/freelance/propertymetrics/* call SetPropertyMetricsOptions()
function SetPropertyMetricsOptions()
    let g:test#project_root = "/home/dvcolgan/freelance/propertymetrics/propertymetrics/"
    let g:test#python#runner = 'djangonose'
    nmap <silent> <leader>tn :TestNearest -s --nologcapture --keepdb<CR>
    nmap <silent> <leader>tf :TestFile -s --nologcapture --keepdb<CR>
    nmap <silent> <leader>ts :TestSuite -s --nologcapture --keepdb<CR>
    nmap <silent> <leader>tl :TestLast -s --nologcapture --keepdb<CR>
    nmap <silent> <leader>tv :TestVisit -s --nologcapture --keepdb<CR>
endfunction

autocmd BufRead,BufNewFile /home/dvcolgan/freelance/loantrac/* call SetLoantracOptions()
function SetLoantracOptions()
    nmap <silent> <leader>tn :TestNearest --keepdb<CR>
    nmap <silent> <leader>tf :TestFile --keepdb<CR>
    nmap <silent> <leader>ts :TestSuite --keepdb<CR>
    nmap <silent> <leader>tl :TestLast --keepdb<CR>
    nmap <silent> <leader>tv :TestVisit --keepdb<CR>
endfunction

autocmd BufRead,BufNewFile /home/dvcolgan/freelance/drivendata-platform/* call SetDrivenDataPlatformOptions()
function SetDrivenDataPlatformOptions()
    nmap <silent> <leader>tn :TestNearest --keepdb<CR>
    nmap <silent> <leader>tf :TestFile --keepdb<CR>
    nmap <silent> <leader>ts :TestSuite --keepdb<CR>
    nmap <silent> <leader>tl :TestLast --keepdb<CR>
    nmap <silent> <leader>tv :TestVisit --keepdb<CR>
endfunction

autocmd BufRead,BufNewFile /home/dvcolgan/freelance/theme-monitoringlove/* call SetMonitoringLoveOptions()
function SetMonitoringLoveOptions()
    set tabstop=2
    set softtabstop=2
    set shiftwidth=2
endfunction

let g:markdown_mapping_switch_status='<Leader><Space>'

" Don't highlight underscores in red
syn match markdownError "\w\@<=\w\@="
