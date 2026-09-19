#!/bin/zsh
# usage: still.sh <t> <outname> [extra query string]
D=/Users/tk/Desktop/brain/projects/rive/riso-keeper
mkdir -p "$D/out/stills"
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --window-size=720,720 --virtual-time-budget=8000 --screenshot="$D/out/stills/$2.png" "file://$D/index.html?t=$1${3:+&$3}" >/dev/null 2>&1
echo "$D/out/stills/$2.png"
