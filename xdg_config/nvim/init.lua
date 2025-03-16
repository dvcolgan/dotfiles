-- Bootstrap lazy.nvim
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not (vim.uv or vim.loop).fs_stat(lazypath) then
  local lazyrepo = "https://github.com/folke/lazy.nvim.git"
  local out = vim.fn.system({ "git", "clone", "--filter=blob:none", "--branch=stable", lazyrepo, lazypath })
  if vim.v.shell_error ~= 0 then
    vim.api.nvim_echo({
      { "Failed to clone lazy.nvim:\n", "ErrorMsg" },
      { out, "WarningMsg" },
      { "\nPress any key to exit..." },
    }, true, {})
    vim.fn.getchar()
    os.exit(1)
  end
end
vim.opt.rtp:prepend(lazypath)

-- Make sure to setup `mapleader` and `maplocalleader` before
-- loading lazy.nvim so that mappings are correct.
-- This is also a good place to setup other settings (vim.opt)
vim.g.mapleader = ','
vim.g.maplocalleader = "\\"

vim.cmd[[
filetype plugin on
filetype indent on
syntax on
]]

-- Map Ctrl+s to save
vim.keymap.set('n', '<C-s>', ':w<CR>', { noremap = true, silent = true })
vim.keymap.set('i', '<C-s>', '<Esc>:w<CR>', { noremap = true, silent = true })

-- Map Ctrl+Backspace to delete word backward (like Ctrl+W)
vim.keymap.set('i', '<C-BS>', '<C-W>', {noremap = true})
vim.keymap.set('i', '<C-H>', '<C-W>', {noremap = true})  -- For terminal compatibility



vim.opt.shortmess = vim.o.shortmess .. 'c'
vim.opt.hidden = true
vim.opt.whichwrap = 'b,s,<,>,[,],h,l,~'
vim.opt.pumheight = 10
vim.opt.encoding = 'utf-8'
vim.opt.ruler = true
vim.opt.showmode = true
vim.opt.showcmd = true
vim.opt.fileencoding = 'utf-8'
vim.opt.cmdheight = 1
vim.opt.splitbelow = true
vim.opt.splitright = true
vim.opt.termguicolors = true
vim.opt.conceallevel = 0
vim.opt.backup = false
vim.opt.writebackup = false
vim.opt.updatetime = 250
vim.opt.timeoutlen = 300
vim.opt.clipboard = 'unnamedplus'
vim.opt.incsearch = true
vim.opt.ignorecase = true
vim.opt.smartcase = true

vim.opt.numberwidth = 3

vim.opt.scrolloff = 3
--vim.opt.sidescrolloff = 5
vim.opt.mouse = 'a'
vim.opt.wrap = true

vim.opt.backspace = '2'
vim.opt.linebreak = true
vim.opt.textwidth = 0

vim.opt.number = true
vim.opt.cursorline = true
vim.opt.signcolumn = 'yes'
vim.opt.tabstop = 4
vim.opt.softtabstop = 4
vim.opt.shiftwidth = 4
vim.opt.foldenable = false


--vim.opt.indentexpr = ''
--vim.opt.autoindent = true
--vim.opt.smartindent = false
--vim.opt.cindent = false
vim.opt.cinkeys = ''


vim.opt.shiftround = true
vim.opt.expandtab = true


vim.opt.showmatch = true

vim.opt.history = 10000
vim.opt.undolevels = 10000
vim.opt.errorbells = false
vim.opt.hlsearch = true


local function map(mode, shortcut, command)
  vim.api.nvim_set_keymap(mode, shortcut, command, { noremap = true, silent = true })
end

local function nmap(shortcut, command) map('n', shortcut, command) end
local function imap(shortcut, command) map('i', shortcut, command) end
local function vmap(shortcut, command) map('v', shortcut, command) end
local function cmap(shortcut, command) map('c', shortcut, command) end
local function tmap(shortcut, command) map('t', shortcut, command) end

--nmap('<c-c>', '<esc>')
imap('<c-c>', '<esc>')
vmap('<c-c>', '<esc>')

vim.cmd[[
nmap <silent> <leader>ws :%s/\s\+$//e<CR>
]]


-- be able to edit things in the :command line
vim.cmd[[
cnoremap <c-a> <home>
cnoremap <c-e> <end>
cnoremap <c-f> <right>
cnoremap <c-b> <left>
cnoremap <m-f> <c-right>
cnoremap <m-b> <c-left>
cnoremap <c-k> <c-o>C
]]

nmap('<leader>nn', ':NvimTreeToggle<CR>')
nmap('<leader>nf', ':NvimTreeFindFile<CR>')
vim.cmd[=[
no <leader>d A [[<cr>    ---<cr>    ---<cr>]]<esc><up><up>o    <esc>!!date +"timestamp: \%Y-\%m-\%dT\%H:\%M:\%S\%:z"<cr>

iab pdb import ipdb; ipdb.set_trace()

inoremap {<cr> {<cr>}<c-o>O
inoremap {,<cr> {<cr>},<c-o>O
inoremap {;<cr> {<cr>};<c-o>O

inoremap ({<cr> ({<cr>})<c-o>O
inoremap ({,<cr> ({<cr>}),<c-o>O
inoremap ({;<cr> ({<cr>});<c-o>O

inoremap {)<cr> {<cr>})<c-o>O
inoremap {),<cr> {<cr>}),<c-o>O
inoremap {);<cr> {<cr>});<c-o>O

inoremap (<cr> (<cr>)<c-o>O
inoremap (,<cr> (<cr>),<c-o>O
inoremap (;<cr> (<cr>);<c-o>O

"inoremap [<cr> [<cr>]<c-o>O
inoremap [,<cr> [<cr>],<c-o>O
"inoremap [;<cr> [<cr>];<c-o>O

inoremap [{<cr> [{<cr>}]<c-o>O
inoremap [{,<cr> [{<cr>}],<c-o>O
inoremap [{;<cr> [{<cr>}];<c-o>O

inoremap {/*<cr> {/*<cr>*/}<c-o>O<tab>
"inoremap :<cr> :<cr><tab>

]=]


nmap('Y', 'y$')

nmap('<C-l>', '<C-l>zz')
nmap('t', 'gj')
nmap('n', 'gk')
nmap('s', 'l')
-- keep search matches in the middle of the window
nmap('l', 'nzzzv')
nmap('j', 't')
nmap('k', 's')

nmap('T', '}')
nmap('N', '{')
nmap('L', 'Nzzzv')
nmap('J', 'T')
--nmap('K', 'S')
nmap('S', '$')
nmap('H', '^')

vmap('t', 'gj')
vmap('n', 'gk')
vmap('s', 'l')
vmap('l', 'n')
vmap('j', 't')
vmap('k', 's')

vmap('T', '}')
vmap('N', '{')
vmap('L', 'N')
vmap('J', 'T')
vmap('K', 'S')
vmap('S', '$')
vmap('H', '^')

nmap('<leader>h', '<cmd>nohl<cr>')
nmap('<leader><space>', '<cmd>wa<cr>')

nmap('-', 'J')
vmap('-', 'J')
nmap('Q', 'gqap')


-- Make space the wincmd
nmap('<space>', '<c-w>')

nmap('<space>t', '<C-w>j')
nmap('<space>T', '<C-w>J')
nmap('<space>n', '<C-w>k')
nmap('<space>N', '<C-w>K')
nmap('<space>s', '<C-w>l')
nmap('<space>S', '<C-w>L')

nmap('<space>j', '<C-w>t')
nmap('<space>J', '<C-w>T')
nmap('<space>k', '<C-w>n')
nmap('<space>K', '<C-w>N')
nmap('<space>l', '<C-w>s')
nmap('<space>L', '<C-w>S')

nmap('<space><space>', '<cmd>wa<cr>')

nmap('<leader>cl', ':set bg=light<cr>')
nmap('<leader>cd', ':set bg=dark<cr>')
nmap('<leader>cx', ':!chmod +x %<cr>')
nmap('<leader>xx', '<cmd><cr><cmd>source %<cr>')

-- TODO need to get the module name from the path returned by %, or find a way to find the path of the current module
--nmap('<leader>xr', 'R(vim.fn.expand("%"))')




nmap('<C-e>', '3<C-e>')
nmap('<C-y>', '3<C-y>')

imap(',', ',<c-g>u')
imap('.', '.<c-g>u')
imap('!', '!<c-g>u')
imap('?', '?<c-g>u')

nmap('<leader>cn', '<cmd>cnext<cr>')
nmap('<leader>cp', '<cmd>cprevious<cr>')

nmap('<C-p>', '<cmd>Telescope find_files<cr>')
nmap('<C-g>', '<cmd>Telescope live_grep<cr>')
--nmap('<C-?>', '<cmd>Telescope help_tags<cr>')
--nmap('<leader>rf', ':Telescope find_files<cr>')
--nmap('<leader>rg', ':Telescope live_grep<cr>')
--nmap('<leader>rh', ':Telescope help_tags<cr>')


vim.cmd[[
autocmd FileType beancount inoremap . .<C-\><C-O>:AlignCommodity<CR>
autocmd FileType beancount nnoremap <buffer> <leader>= :AlignCommodity<CR>
autocmd FileType beancount vnoremap <buffer> <leader>= :AlignCommodity<CR>
]]


-- Setup lazy.nvim
require("lazy").setup({
    spec = {
        { "ellisonleao/gruvbox.nvim", priority = 1000 , config = true, opts = ...},
        {
            "nvim-tree/nvim-tree.lua",
            version = "*",
            lazy = false,
            dependencies = {
                "nvim-tree/nvim-web-devicons",
            },
            config = function()
                require("nvim-tree").setup {}
            end,
        },
        {
        'nvim-telescope/telescope.nvim', tag = '0.1.8',
          dependencies = { 'nvim-lua/plenary.nvim' }
        },

    },
    -- Configure any other settings here. See the documentation for more details.
    -- colorscheme that will be used when installing plugins.
    install = { colorscheme = { "gruvbox" } },
    -- automatically check for plugin updates
    checker = { enabled = true },
})


vim.g.gruvbox_contrast_dark = 'hard'
vim.g.gruvbox_contrast_light = 'hard'
vim.cmd('colorscheme gruvbox')
vim.opt.background = 'dark'
