" Author: @YorkFish
" Original name: init.vim

" 1. System
let &t_ut=''
set autochdir

" 2. Provider Health
let g:loaded_python_provider = 0
let g:python3_host_prog = 'E:/Anaconda3/python.exe'
let g:loaded_ruby_provider = 0

" 3. Editor Behavior
set number
set cursorline
set expandtab
set tabstop=4
set shiftwidth=4
set softtabstop=4
set autoindent
set textwidth=0
set indentexpr=
set list
set listchars=tab:\|\ ,trail:▫
set scrolloff=4
set foldmethod=indent
set foldlevel=99
set foldenable
set wildmenu
set ignorecase
set smartcase
set ttimeoutlen=0
set notimeout
set viewoptions=cursor,folds,slash,unix
set formatoptions-=tc
set splitright
set splitbelow
set noshowmode
set showcmd
set shortmess+=c
set inccommand=split
set ttyfast
set lazyredraw
set visualbell
set colorcolumn=80
set updatetime=1000
set virtualedit=block
set fillchars=vert:\ ,stl:\ ,stlnc:\
au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif

" 4. Basic Mappings
let mapleader=" "
noremap ; :
noremap Q :q<CR>
noremap <C-q> :qa<CR>
noremap S :w<CR>
nnoremap Y y$
vnoremap Y "+y
nnoremap < <<
nnoremap > >>
noremap <LEADER><CR> :nohlsearch<CR>
noremap <LEADER>dw /\(\<\w\+\>\)\_s*\1
nnoremap <LEADER>tt :%s/    /\t/g
vnoremap <LEADER>tt :s/    /\t/g
noremap <silent> <LEADER>o za
noremap <LEADER>rc :e ~/AppData/Local/nvim/init.vim<CR>

" 5. Cursor Movement
noremap <silent> K 5k
noremap <silent> J 5j
noremap <silent> H 0
noremap <silent> L $
noremap W 5w
noremap B 5b
noremap <C-U> 5<C-y>
noremap <C-E> 5<C-e>

" 6. Insert Mode Cursor Movement
inoremap <C-a> <ESC>A

" 7. Window management
noremap <LEADER>w <C-w>w
noremap <LEADER>k <C-w>k
noremap <LEADER>j <C-w>j
noremap <LEADER>h <C-w>h
noremap <LEADER>l <C-w>l
noremap s <nop>
noremap sk :set nosplitbelow<CR>:split<CR>:set splitbelow<CR>
noremap sj :set splitbelow<CR>:split<CR>
noremap sh :set nosplitright<CR>:vsplit<CR>:set splitright<CR>
noremap sl :set splitright<CR>:vsplit<CR>
noremap <up> :res +5<CR>
noremap <down> :res -5<CR>
noremap <left> :vertical resize-5<CR>
noremap <right> :vertical resize+5<CR>
noremap sf <C-w>t<C-w>K
noremap sv <C-w>t<C-w>H
noremap <LEADER>q <C-w>j:q<CR>
noremap nr :set relativenumber<CR>
noremap nn :set norelativenumber<CR>

" 8. Tab management
noremap tu :tabe<CR>
noremap tn :-tabnext<CR>
noremap ti :+tabnext<CR>
noremap tmn :-tabmove<CR>
noremap tmi :+tabmove<CR>

" 9. colorscheme
set termguicolors
let $NVIM_TUI_ENABLE_TRUE_COLOR=1
colorscheme molokai
let g:molokai_original = 1

" 10. Markdown Settings
source ~/AppData/Local/nvim/md-snippets.vim
autocmd BufRead,BufNewFile *.md setlocal spell

" 11. spell check
map <LEADER>sc :set spell!<CR>

" 12. Compile function
noremap m :call CompileRunGcc()<CR>
func! CompileRunGcc()
    exec "w"
    if &filetype == 'c'
        exec "!gcc -std=c11 % -o %<"
        exec "!%<"
    elseif &filetype == 'cpp' || &filetype == 'cc'
        exec "!g++ -Wall -std=c++14 % -o %<"
        exec "!%<"
    elseif &filetype == 'python'
        :sp
        :term python %
    elseif &filetype == 'markdown'
        exec "MarkdownPreview"
    endif
endfunc


" ====
" === Install Plugins with Vim-Plug
" ====
call plug#begin('~/.vim/plugged')

" Bottom status bar
Plug 'vim-airline/vim-airline'
" Left menu bar
Plug 'preservim/nerdtree'
" Error checking
Plug 'w0rp/ale'
" Python
Plug 'vim-scripts/indentpython.vim'
" Markdown-preview
Plug 'iamcco/markdown-preview.nvim', { 'do': { -> mkdp#util#install_sync() }, 'for' :['markdown', 'vim-plug'] }

call plug#end()

" === NERDTree
map tt :NERDTreeToggle<CR>
let NERDTreeMapOpenExpl = ""
let NERDTreeMapUpdir = ""
let NERDTreeMapUpdirKeepOpen = "l"
let NERDTreeMapOpenSplit = ""
let NERDTreeOpenVSplit = ""
let NERDTreeMapActivateNode = "i"
let NERDTreeMapOpenInTab = "o"
let NERDTreeMapPreview = ""
let NERDTreeMapCloseDir = "n"
let NERDTreeMapChangeRoot = "y"

" === ale
let b:ale_linters = ['pylint']
let b:ale_fixers = ['autopep8', 'yapf']

" === MarkdownPreview
let g:mkdp_auto_start = 0
let g:mkdp_auto_close = 1
let g:mkdp_refresh_slow = 0
let g:mkdp_command_for_global = 0
let g:mkdp_open_to_the_world = 0
let g:mkdp_open_ip = ''
let g:mkdp_browser = ''
let g:mkdp_echo_preview_url = 0
let g:mkdp_browserfunc = ''
let g:mkdp_preview_options = {
    \ 'mkit': {},
    \ 'katex': {},
    \ 'uml': {},
    \ 'maid': {},
    \ 'disable_sync_scroll': 0,
    \ 'sync_scroll_type': 'middle',
    \ 'hide_yaml_meta': 1
    \ }
let g:mkdp_markdown_css = ''
let g:mkdp_highlight_css = ''
let g:mkdp_port = ''
let g:mkdp_page_title = '「${name}」'

" MarkdownPreview on & off
nmap <C-s> <Plug>MarkdownPreview
nmap <A-s> <Plug>MarkdownPreviewStop
