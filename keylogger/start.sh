#!/usr/bin/env bash
# Make sure you have `logkeys` installed
# sudo apt-get install logkeys

#sudo logkeys -m $(pwd)/keymaps/en_GB.map -o $(pwd)/log/keys.log -s
scriptDir=$(dirname -- "$(readlink -e -- "$BASH_SOURCE")")

cd "$scriptDir"
sudo logkeys -m keymaps/kek.map -o log/keys.log -s
