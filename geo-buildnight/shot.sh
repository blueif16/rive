#!/bin/zsh
# usage: shot.sh <t> [outname] [extra query]   → out/stills/<name>.png via headless Chrome
t=$1; name=${2:-t$(echo $t | tr . _)}; q=$3
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --window-size=1280,720 --virtual-time-budget=8000 --screenshot="/Users/tk/Desktop/brain/projects/rive/geo-buildnight/out/stills/$name.png" "file:///Users/tk/Desktop/brain/projects/rive/geo-buildnight/index.html?t=$t$q" >/dev/null 2>&1
