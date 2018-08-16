set nocompatible
filetype off

set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

Plugin 'VundleVim/Vundle.vim'

" Colors
Plugin 'nanotech/jellybeans.vim'
Plugin 'reedes/vim-colors-pencil'


" IDE things
Plugin 'kien/ctrlp.vim'
Plugin 'scrooloose/nerdtree'
Plugin 'janko-m/vim-test'
Plugin 'w0rp/ale'
Plugin 'Shougo/deoplete.nvim'
Plugin 'SirVer/ultisnips'
"Plugin 'honza/vim-snippets'

" Javascript
"Plugin 'pangloss/vim-javascript'
"Plugin 'othree/yajs.vim'
"Plugin 'othree/es.next.syntax.vim'
"Plugin 'mxw/vim-jsx'
Plugin 'chemzqm/vim-jsx-improve'
Plugin 'posva/vim-vue'

" HTML and CSS
Plugin 'ap/vim-css-color' 
Plugin 'mattn/emmet-vim'

" Markdown
Plugin 'plasticboy/vim-markdown'
"Plugin 'gabrielelana/vim-markdown'
"Plugin 'tpope/vim-markdown'
"Plugin 'nelstrom/vim-markdown-folding'
Plugin 'vim-voom/VOoM'

" Typescript
Plugin 'leafgarland/typescript-vim'

" Elixir
Plugin 'elixir-editors/vim-elixir'
Plugin 'slashmili/alchemist.vim'

" Python
Plugin 'hynek/vim-python-pep8-indent'
Plugin 'niftylettuce/vim-jinja'
"Plugin 'davidhalter/jedi-vim'
"Plugin 'zchee/deoplete-jedi'

" C#
"Plugin 'OmniSharp/omnisharp-vim'


call vundle#end()
filetype plugin indent on
syntax on

au BufRead,BufNewFile *.ts  setlocal filetype=typescript
let g:vim_markdown_fenced_languages = ['python=python', 'bash=sh']
let g:vim_markdown_folding_disabled = 1

autocmd FileType markdown no <enter> za
"autocmd FileType markdown no <tab> >>
"autocmd FileType markdown no <s-tab> <<
let g:voom_return_key = "<Tab>"
let g:voom_tab_key = "<C-Tab>"
let g:voom_tree_width = 60
let g:voom_default_mode = 'markdown'
let g:voom_always_allow_move_left = 1


"Plugin 'w0rp/ale'
let g:ale_lint_on_save = 1
let g:ale_lint_on_text_changed = 0
let g:ale_completion_enabled = 1
let g:ale_fixers = {
\    'javascript': ['eslint']
\}

"let g:ale_linters = {
"\   'elixir': ['dogma']
"\}

"let g:tsuquyomi_disable_quickfix = 1
"let g:syntastic_typescript_checkers = ['tsuquyomi']
"let g:tsuquyomi_completion_detail = 1

let g:UltiSnipsExpandTrigger="<tab>"

"let g:UltiSnipsJumpForwardTrigger="c-b"
"let g:UltiSnipsJumpBackwardTrigger="c-f"
let g:UltiSnipsSnippetDirectories=[$HOME.'/.vim/UltiSnips']


"let g:syntastic_python_checkers = ['flake8']

"let g:javascript_plugin_flow = 1
"let g:jsx_ext_required = 0
"let g:syntastic_javascript_checkers = ['eslint', 'flow']
"let g:syntastic_javascript_flow_exe = 'flow'
"let g:syntastic_javascript_eslint_exec = 'eslint_d'
"let g:ale_linters = {
"\   'javascript': ['eslint']
"\}
"let g:flow#enable = 0

let g:ctrlp_follow_symlinks = 1
let g:ctrlp_custom_ignore = '\v[\/](output|env|dist|staticfiles|node_modules|__pycache__|deps|_build)|(\.(swp|git|png|jpg|pyc))$'



"set statusline+=%#warningmsg#
"set statusline+=%{SyntasticStatuslineFlag()}
"set statusline+=%*
"
"
"let g:syntastic_vue_checkers = ['eslint']
"let g:syntastic_vue_eslint_exec = 'eslint_d'
"autocmd BufRead,BufNewFile *.vue setlocal filetype=vue.html.javascript.css

autocmd BufRead,BufNewFile *.mjs setlocal filetype=javascript

let mapleader = ","
set nocompatible " Vim rather than Vi
set termguicolors

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
no <leader>D !!date +"\%A \%B \%d, \%Y \%r"<cr>
no <leader>d !!date +"\%B \%d, \%Y"<cr>
no <leader>d !!date +"\%B \%d, \%Y"<cr>
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

no <leader>nf :NERDTreeFind<cr>

vnoremap y "*y


 let g:NERDTreeMapOpenInTab = ''
 let NERDTreeIgnore = ['\.pyc$']

" Allow creating a directory and file at the same time
augroup vimrc-auto-mkdir
  autocmd!
  autocmd BufWritePre * call s:auto_mkdir(expand('<afile>:p:h'), v:cmdbang)
  function! s:auto_mkdir(dir, force)
    if !isdirectory(a:dir)
          \   && (a:force
          \       || input("'" . a:dir . "' does not exist. Create? [y/N]") =~? '^y\%[es]$')
      call mkdir(iconv(a:dir, &encoding, &termencoding), 'p')
    endif
  endfunction
augroup END

"set noswapfile
" Set swapfile storage directory
set directory^=$HOME/.vim/tmp//


ino <C-c> <esc>
no <SPACE> <C-w>
no <SPACE>h <C-w>h
no <SPACE>t <C-w>j
no <SPACE>n <C-w>k
no <SPACE>s <C-w>l

imap <F4> {}<UP>zzo
imap <F5> {}<UP>zzo
imap <F6> {});<UP>zzo
"imap <leader>e= <%=  %><left><left><left>
"imap <leader>e <% %><left><left><left>

" TECHNICAL
set mouse=a
set encoding=utf-8
set fileencoding=utf-8
set termencoding=utf-8

set autoindent
set smartindent
au Filetype markdown setlocal tabstop=4 softtabstop=4 shiftwidth=4
au Filetype yaml setlocal tabstop=2 softtabstop=2 shiftwidth=2
au filetype elm call DisableIndent()
autocmd FileType markdown,text setlocal spell

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

"set term=xterm-256color
iab pdb import ipdb; ipdb.set_trace()
iab rdb ((val: any) => { console.log(val); return val; })(

iab rcc class extends Component {render() {return ();}};

"nnoremap <leader>el :ElmEvalLine<CR>
"vnoremap <leader>es :<C-u>ElmEvalSelection<CR>
"nnoremap <leader>em :ElmMakeCurrentFile<CR>
no <space>l :!love .<cr>

nnoremap <space>r :let _s=@/<Bar>:%s/\s\+$//e<Bar>:let @/=_s<Bar><CR>


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

"autocmd FileType javascript set formatprg=prettier\ --stdin
"autocmd BufWritePre *.js :normal magggqG'a

" Fix syntax highlighting breaking in vue files among others
autocmd BufEnter *.vue :syntax sync fromstart
autocmd BufEnter *.html :syntax sync fromstart




" vim-test
nmap <silent> <leader>tN :TestNearest<CR>
nmap <silent> <leader>tF :TestFile<CR>
nmap <silent> <leader>tS :TestSuite<CR>
nmap <silent> <leader>tL :TestLast<CR>
nmap <silent> <leader>tV :TestVisit<CR>

nmap <silent> <leader>tn :TestNearest --keepdb<CR>
nmap <silent> <leader>tf :TestFile --keepdb<CR>
nmap <silent> <leader>ts :TestSuite --keepdb<CR>
nmap <silent> <leader>tl :TestLast --keepdb<CR>
nmap <silent> <leader>tv :TestVisit --keepdb<CR>


let test#strategy = "neovim"
let test#python#pytest#options = '--capture=no'

autocmd BufRead,BufNewFile /home/dvcolgan/projects/propertymetrics/* call SetPropertyMetricsOptions()
function SetPropertyMetricsOptions()
    let g:test#project_root = "/home/dvcolgan/projects/propertymetrics/propertymetrics/"
    let g:test#python#runner = 'djangonose'
    nmap <silent> <leader>tn :TestNearest -s --nologcapture --keepdb<CR>
    nmap <silent> <leader>tf :TestFile -s --nologcapture --keepdb<CR>
    nmap <silent> <leader>ts :TestSuite -s --nologcapture --keepdb<CR>
    nmap <silent> <leader>tl :TestLast -s --nologcapture --keepdb<CR>
    nmap <silent> <leader>tv :TestVisit -s --nologcapture --keepdb<CR>
endfunction

let g:markdown_mapping_switch_status='<Leader><Space>'


set synmaxcol=0

" Rename current file from Gary Bernhardt
function! RenameFile()
    let old_name = expand('%')
    let new_name = input('New file name: ', expand('%'), 'file')
    if new_name != '' && new_name != old_name
        exec ':saveas ' . new_name
        exec ':silent !rm ' . old_name
        redraw!
    endif
endfunction
map <leader>rf :call RenameFile()<cr>
