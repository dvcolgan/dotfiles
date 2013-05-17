set nocompatible | filetype indent plugin on | syn on

fun! EnsureVamIsOnDisk(plugin_root_dir)
    let vam_autoload_dir = a:plugin_root_dir.'/vim-addon-manager/autoload'
    if isdirectory(vam_autoload_dir)
    return 1
    else
    if 1 == confirm("Clone VAM into ".a:plugin_root_dir."?","&Y\n&N")
        call confirm("Remind yourself that most plugins ship with ".
                    \"documentation (README*, doc/*.txt). It is your ".
                    \"first source of knowledge. If you can't find ".
                    \"the info you're looking for in reasonable ".
                    \"time ask maintainers to improve documentation")
        call mkdir(a:plugin_root_dir, 'p')
        execute '!git clone --depth=1 git://github.com/MarcWeber/vim-addon-manager '.
                    \       shellescape(a:plugin_root_dir, 1).'/vim-addon-manager'
        exec 'helptags '.fnameescape(a:plugin_root_dir.'/vim-addon-manager/doc')
    endif
    return isdirectory(vam_autoload_dir)
    endif
endfun

fun! SetupVAM()
    let c = get(g:, 'vim_addon_manager', {})
    let g:vim_addon_manager = c
    let c.plugin_root_dir = expand('$HOME/.vim/vim-addons')
    if !EnsureVamIsOnDisk(c.plugin_root_dir)
    echohl ErrorMsg | echomsg "No VAM found!" | echohl NONE
    return
    endif
    let &rtp.=(empty(&rtp)?'':',').c.plugin_root_dir.'/vim-addon-manager'

     
    call vam#ActivateAddons([
        \"github:ap/vim-css-color", 
        \"github:jeroenbourgois/vim-actionscript", 
        \"github:groenewege/vim-less",
        \"github:kchmck/vim-coffee-script",
        \"github:kien/ctrlp.vim",
        \"github:nanotech/jellybeans.vim",
        \"github:jdonaldson/vaxe"
        \], {'auto_install' : 1})
endfun
call SetupVAM()

let mapleader = ","

let g:SuperTabDefaultCompletionType = "<c-x><c-o>"
let g:SuperTabClosePreviewOnPopupClose = 1
let g:ctrlp_working_path_mode = 'w'

"if !exists('g:neocomplcache_omni_patterns')
"    let g:neocomplcache_omni_patterns = {}
"endif
"let g:neocomplcache_omni_patterns.haxe = '\v([\]''"]|\w)(\.|\()'
"let g:neocomplcache_enable_at_startup = 1

"let g:vaxe_nme_target = "cpp"

let g:ctrlp_match_window_bottom = 1
let g:ctrlp_max_height = 20 
let g:ctrlp_clear_cache_on_exit = 0
set wildignore+=*/.git/*,*/.hg/*,*/.svn/*,*/bin/*,*.pyc,*.js
let g:ctrlp_follow_symlinks = 1

set nocompatible " Vim rather than Vi
set t_Co=256 " force 256 colors in terminal

set bg=dark
set linebreak

" APPEARANCE
syntax enable
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

set shiftround                      " Round indents to multiples of shiftwidth

set autoindent
set smartindent
set expandtab
set smarttab

set backspace=2
set showmatch
set pastetoggle=<F12>

set history=200
set undolevels=200
set ttyfast		                    " smoother output, they claim
set whichwrap=h,l,~,[,]

set incsearch
set noerrorbells
set hlsearch


nnoremap <C-e> 3<C-e>
nnoremap <C-y> 3<C-y>
no <space><space> :wa<cr> :w<cr>
no <leader>d !!date +"\%A \%B \%d, \%Y \%r"<cr>
no <leader>v :vsp $MYVIMRC<cr>
no <leader>s :source $MYVIMRC<cr>

no <leader>n :cnext<cr>
no <leader>p :cprevious<cr>

no <F5> :make<cr>

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



" TECHNICAL
set mouse=a
set encoding=utf-8
set fileencoding=utf-8
set termencoding=utf-8

"au BufRead,BufNewFile *.hx set filetype=haxe
"au! Syntax haxe source /home/dcolgan/.vim/syntax/haxe.vim

"au BufRead,BufNewFile *.less set filetype=css
"au BufRead,BufNewFile *.coffee set filetype=coffee
"au! Syntax coffee source ~/.vim/syntax/coffee.vim


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

colorscheme jellybeans



:python << EOF
import os
virtualenv = os.environ.get('VIRTUAL_ENV')
if virtualenv:
    activate_this = os.path.join(virtualenv, 'bin', 'activate_this.py')
    if os.path.exists(activate_this):
        execfile(activate_this, dict(__file__=activate_this))
EOF
