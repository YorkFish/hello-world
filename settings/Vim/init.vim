" Author: @YorkFish

" 1. System
let &t_ut=''
set autochdir

" 2. Provider Health
let g:loaded_python_provider = 0
let g:python3_host_prog = 'D:/anaconda3/python.exe'
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
set colorcolumn=80
set foldmethod=indent
set foldlevel=99
set foldenable
set wildmenu
set ttimeoutlen=0
set notimeout
set viewoptions=cursor,folds,slash,unix
set ttyfast
set lazyredraw
set visualbell
set updatetime=1000
set virtualedit=block
set encoding=utf-8
set guifont=Cascadia\ Code\ PL:h16
set formatoptions-=tc
set ignorecase
set smartcase
set noshowmode
set showcmd
set shortmess+=c
set inccommand=split
set splitright
set splitbelow
set fillchars=vert:\ ,stl:\ ,stlnc:\
au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif

" 4. Basic Mappings
noremap ; :
noremap Q :q<CR>
noremap <C-q> :qa<CR>
noremap S :w<CR>
nnoremap > >>

let mapleader=" "
nnoremap Y y$
vnoremap Y "+y
nnoremap <Leader>p "+p
nnoremap <LEADER>tt :%s/    /\t/g
vnoremap <LEADER>tt :s/    /\t/g
noremap <LEADER><CR> :nohlsearch<CR>
noremap <LEADER>dw /\(\<\w\+\>\)\_s*\1
noremap <silent> <LEADER>o za
noremap <LEADER>rc :e ~/AppData/Local/nvim/init.vim<CR>
noremap R :source $MYVIMRC<CR>

" 5. Cursor Movement
noremap <silent> J 5j
noremap <silent> H 0
noremap <silent> L $
noremap W 5w
noremap B 5b
noremap sr :set relativenumber<CR>
noremap sn :set norelativenumber<CR>

" 6. Insert Mode Cursor
inoremap jk <Esc>
inoremap <C-a> <ESC>A

" 7. Window management
noremap <C-U> 5<C-y>
noremap <C-E> 5<C-e>
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
noremap st :set splitright<CR>:vsplit<CR>:term<CR>3jA

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

" 12. one click execution
noremap <A-3> :s/^/# /<CR>
noremap <A-4> :s/^# //<CR>
noremap <F6> :w<CR>:!python %<CR>
noremap <F7> :w<CR>:!pycodestyle %<CR>
noremap <A-5> :!gcc -Wall %<CR>
noremap <A-6> :!a.exe<CR>

" 13. Compile function
noremap m :call CompileRun()<CR>
func! CompileRun()
    exec "w"
    if &filetype == 'c'
        exec "!gcc -Wall -finput-charset=utf-8 -fexec-charset=gbk % -o %<"
        :!start cmd /c "%< & pause"
    elseif &filetype == 'cpp' || &filetype == 'cc'
        exec "!g++ -Wall -std=c++11 -finput-charset=utf-8 % -o %<"
        exec "!%<"
    elseif &filetype == 'python'
        set splitbelow
        :sp
        :term python %
    endif
endfunc

" === VimPlugins
call plug#begin('~/.vim/plugged')
Plug 'vim-airline/vim-airline'
Plug 'preservim/nerdtree'
Plug 'neoclide/coc.nvim', {'branch': 'release'}
call plug#end()

" nerdtree
map <C-k> :NERDTreeToggle<CR>
let g:NERDTreeDirArrowExpandable = '►'
let g:NERDTreeDirArrowCollapsible = '▼'
let NERDTreeAutoCenter=1
let NERDTreeShowLineNumbers=1

" Coc.nvim
set hidden

inoremap <silent><expr> <TAB>
      \ pumvisible() ? "\<C-n>" :
      \ <SID>check_back_space() ? "\<TAB>" :
      \ coc#refresh()
inoremap <expr><S-TAB> pumvisible() ? "\<C-p>" : "\<C-h>"

function! s:check_back_space() abort
  let col = col('.') - 1
  return !col || getline('.')[col - 1]  =~# '\s'
endfunction

inoremap <silent><expr> <s-space> coc#refresh()
nmap <silent> <LEADER>- <Plug>(coc-diagnostic-prev)
nmap <silent> <LEADER>+ <Plug>(coc-diagnostic-next)
nmap <silent> gd <Plug>(coc-definition)
nmap <silent> gy <Plug>(coc-type-definition)
nmap <silent> gi <Plug>(coc-implementation)
nmap <silent> gr <Plug>(coc-references)

" Use `<space>h` to show documentation in preview window.
nnoremap <silent> <LEADER>h :call <SID>show_documentation()<CR>
function! s:show_documentation()
  if (index(['vim','help'], &filetype) >= 0)
    execute 'h '.expand('<cword>')
  else
    call CocActionAsync('doHover')
  endif
endfunction

" Symbol renaming.
nmap <leader>rn <Plug>(coc-rename)
