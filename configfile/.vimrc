"This is the personal .vimrc file of Ryan Duan.
"Thanks for Steve's spf13.
"         ____
"        |  _ \
"        | |_) |                  _
"        | |__/    ______  _____ (_)
"        | | \`\  / / _` \/  _` \ /
"        | |  \ \/ / (_) || | | |
"        |_|   \  / \__/\_\_| |_|
"              / /
"             /_/
"
"


" Initializing {
    syntax on                   " Syntax highlighting
    set magic
    vmap <C-c> "+y
    set mouse=a                 " Automatically enable mouse usage
    set mousehide               " Hide the mouse cursor while typing
    scriptencoding utf-8
    set virtualedit=onemore             " Allow for cursor beyond last character
    set history=1000                    " Store a ton of history (default is 20)
"    set spell spelllang=en_us           " Spell checking on
    set hidden                          " Allow buffer switching without saving
    set showmode                    " Display the current mode
    set cursorline                  " Highlight current line
    set ruler                   " Show the ruler
    set rulerformat=%30(%=\:b%n%y%m%r%w\ %l,%c%V\ %P%) " A ruler on steroids
    set showcmd                 " Show partial commands in status line and
    set backspace=indent,eol,start  " Backspace for dummies
    set linespace=0                 " No extra spaces between rows
    set nu                          " Line numbers on
    set showmatch                   " Show matching brackets/parenthesis
    set incsearch                   " Find as you type search
    set hlsearch                    " Highlight search terms
    set winminheight=0              " Windows can be 0 line high
    set ignorecase                  " Case insensitive search
    set smartcase                   " Case sensitive when uc present
    set wildmenu                    " Show list instead of just completing
    set wildmode=list:longest,full  " Command <Tab> completion, list matches, then longest common part, then all.
    set whichwrap=b,s,h,l,<,>,[,]   " Backspace and cursor keys wrap too
    set scrolljump=5                " Lines to scroll when cursor leaves screen
    set scrolloff=3                 " Minimum lines to keep above and below cursor
    set foldenable                  " Auto fold code
    set list
    set listchars=tab:›\ ,trail:•,extends:#,nbsp:. " Highlight problematic whitespace
    set nowrap                      " Wrap long lines
    set autoindent                  " Indent at the same level of the previous line
    set smartindent                 " Smart indent for new line
    set shiftwidth=4                " Use indents of 4 spaces
    set expandtab                   " Tabs are spaces, not tabs
    set tabstop=4                   " An indentation every four columns
    set softtabstop=4               " Let backspace delete indent
    set nojoinspaces                " Prevents inserting two spaces after punctuation on a join (J)
    set splitright                  " Puts new vsplit windows to the right of the current
    set splitbelow                  " Puts new split windows to the bottom of the current
    set pastetoggle=<F12>           " pastetoggle (sane indentation on pastes)

    " Add at 2014-01-27
    set t_Co=256
    colorscheme delek

" }


