#!/bin/bash

# $1 = relative file path
# $2 = session name

tabName="Helix"
sessionName="Helix"

if test -z "$1"
then
  echo "File name not provided"
  exit 1
fi

fileName=$(readlink -f $1) # full path to file

if ! test -z "$2"
then
  sessionName="$2"
fi

if ! pgrep -x helix > /dev/null
then
	echo "1234"
  zellij -s "$sessionNamex
	" action go-to-tab-name $tabName --create
  sleep 0.5
  zellij -s "$sessionName" action write-chars "helix"
  sleep 0.5
  zellij -s "$sessionName" action write 13 # send enter-key
fi



echo "...go to tab ${tabName} in session ${sessionName}..."
zellij -s "$sessionName" action go-to-tab-name $tabName --create
echo "...press ESC... "
sleep 0.1
zellij -s "$sessionName" action write 27 # send escape-key
echo "...open documenti command..."
sleep 0.1
zellij -s "$sessionName" action write-chars ":open $fileName"
echo "...press enter..."
sleep 0.1
zellij -s "$sessionName" action write 13 # send enter-key
