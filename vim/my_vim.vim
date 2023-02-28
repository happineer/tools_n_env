" Filename: C:/Program Files (x86)/Vim/vim90/my_vim.vim

" VIM Color Theme
colorscheme desert

" set the directory where temp file is stored
set backupdir=D:/Programs/vim/temp   "
set directory=D:/Programs/vim/temp   "<filename>~
set undodir=D:/Programs/vim/temp     "<filename>.un~

" various settings
set number        "줄번호

set autoindent    "자동 들여쓰기
set cindent       "C언어 자동 들여쓰기
set tabstop=4     "tab 크기
set expandtab     "tab 을 space 로 확장
set shiftwidth=4  ">>, << 할때 스페이스 갯수(4)

set ruler         "현재 커서 위치 표시

set hlsearch      "검색어 하이라이팅
set incsearch     "
set nowrapscan    "검색할 때 문서의 끝에서 처음으로 안돌아감

set paste         " 붙여넣기 계단현상 없애기

set history=1000  "vi 편집기록 기억갯수 .viminfo에 기록
set fencs=ucs-bom,utf-8,euc-kr.latin1  "한글 파일은 euc-kr로, 유니코드는 유니코드로
set fileencoding=utf-8                 "파일저장인코딩

set sw=1          "스크롤바 너비
set scrolloff=4

" 구문 강조
if has("syntax")
 syntax on
endif
