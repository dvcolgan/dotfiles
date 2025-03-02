syntax clear

" Define syntax groups for each indentation level with proper pattern matching
syntax match NoIndentColor /^\%(\s*\n\)\@<=\%(\s\{0\}.*\|\s*\)$\|\%(^\s\{0\}.*\)$/
syntax match RedColor /^\%(\s*\n\)\@<=\%(\s\{4\}.*\|\s*\)$\|\%(^\s\{4\}.*\)$/
syntax match OrangeColor /^\%(\s*\n\)\@<=\%(\s\{8\}.*\|\s*\)$\|\%(^\s\{8\}.*\)$/
syntax match YellowColor /^\%(\s*\n\)\@<=\%(\s\{12\}.*\|\s*\)$\|\%(^\s\{12\}.*\)$/
syntax match GreenColor /^\%(\s*\n\)\@<=\%(\s\{16\}.*\|\s*\)$\|\%(^\s\{16\}.*\)$/
syntax match BlueColor /^\%(\s*\n\)\@<=\%(\s\{20\}.*\|\s*\)$\|\%(^\s\{20\}.*\)$/
syntax match PurpleColor /^\%(\s*\n\)\@<=\%(\s\{24\}.*\|\s*\)$\|\%(^\s\{24\}.*\)$/
syntax match NoStyleColor /^\%(\s*\n\)\@<=\%(\s\{28\}.*\|\s*\)$\|\%(^\s\{28\}.*\)$/

" Define syntax group for pipe character and following text
syntax match CardPipe /\v(^\s*\|)|(\/\/\|)|(\/\*---)|(---\*\/).+/

" Define custom highlighting with hardcoded hex colors (bold with background colors)
highlight NoIndentColor gui=bold guifg=#FFFFFF guibg=#303030
highlight RedColor gui=bold guifg=#FFFFFF guibg=#880000
highlight OrangeColor gui=bold guifg=#FFFFFF guibg=#AA5500
highlight YellowColor gui=bold guifg=#FFFFFF guibg=#AAAA00
highlight GreenColor gui=bold guifg=#FFFFFF guibg=#008800
highlight BlueColor gui=bold guifg=#FFFFFF guibg=#000088
highlight PurpleColor gui=bold guifg=#FFFFFF guibg=#AA00AA
highlight NoStyleColor gui=bold guifg=#FFFFFF guibg=#303030
highlight CardPipe gui=bold guifg=#FFFFFF guibg=#000000

" Create a cluster of all our custom syntax groups
syntax cluster cardSyntax contains=NoIndentColor,RedColor,OrangeColor,YellowColor,GreenColor,BlueColor,PurpleColor,NoStyleColor,CardPipe

" Set the syntax for the buffer
let b:current_syntax = "card"